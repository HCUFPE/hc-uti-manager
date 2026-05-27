from typing import List, Dict, Any, Optional
from fastapi import HTTPException
from providers.implementations.solicitacao_alta_provider import SolicitacaoAltaProvider
import logging
from datetime import timedelta

logger = logging.getLogger(__name__)

class AltasController:
    """
    Controller para gerenciar solicitações de alta da UTI.
    Combina dados do AGHU (para identificar o paciente no leito) com o estado local (SQLite).
    """

    def __init__(self, alta_provider: SolicitacaoAltaProvider, leitos_controller: Any, estado_provider: Any = None, historico_provider: Any = None):
        self.alta_provider = alta_provider
        self.leitos_controller = leitos_controller
        self.estado_provider = estado_provider
        self.historico_provider = historico_provider

    async def listar_altas(self) -> List[Dict[str, Any]]:
        """Retorna todas as solicitações de alta (ativas), enriquecidas com dados dos leitos."""
        leitos = await self.leitos_controller.listar_leitos()
        leitos_map = {l["lto_lto_id"]: l for l in leitos}

        altas = await self.alta_provider.get_todas()
        resultado = []

        for alta in altas:
            # Filtra apenas as ativas para a listagem principal
            if alta.status not in ["pendente", "definida"]:
                continue

            lto_id_norm = str(alta.lto_id).strip().upper()
            leito_info = leitos_map.get(lto_id_norm, {})
            
            # Tenta recuperar o prontuário se estiver N/D (comum em leitos mockados)
            prontuario = alta.prontuario
            if (prontuario == "N/D" or not prontuario) and leito_info.get("prontuario_atual"):
                prontuario = str(leito_info["prontuario_atual"])

            paciente_nome = leito_info.get("nome_atual") or leito_info.get("nome_paciente", "")
            especialidade = leito_info.get("especialidade_atual", "")

            resultado.append({
                "id": str(alta.id),
                "prontuario": prontuario,
                "nomePaciente": paciente_nome,
                "especialidade": especialidade,
                "leitoAtual": alta.lto_id,
                "leitoDestino": alta.leito_destino or "Pendente (NIR)",
                "dataHora": (alta.criado_em - timedelta(hours=3)).strftime("%d-%m-%Y %H:%M") if alta.criado_em else "",
                "necessidadesEspeciais": alta.necessidades_especiais or "",
                "status": alta.status,
                "destinoDisponivel": bool(alta.destino_disponivel)
            })

        return resultado

    async def solicitar_alta(self, lto_id: str, payload: dict = None) -> dict:
        """
        Registra o pedido de alta para um leito.
        Busca o paciente atual no AGHU e vincula à solicitação.
        """
        payload = payload or {}
        # Verifica se já existe uma solicitação ativa para o leito
        pendente = await self.alta_provider.get_por_lto_id(lto_id)
        if pendente:
            raise HTTPException(
                status_code=400,
                detail=f"Já existe uma solicitação de alta ativa para o leito {lto_id}."
            )

        # Identifica prontuário atual do paciente (incluindo mocks)
        leitos = await self.leitos_controller.listar_leitos()
        leito_info = next((l for l in leitos if l["lto_lto_id"] == lto_id), None)
        prontuario = str(leito_info["prontuario_atual"]) if leito_info and leito_info.get("prontuario_atual") else "N/D"

        nova_alta = {
            "lto_id": lto_id,
            "prontuario": prontuario,
            "leito_destino": None,
            "necessidades_especiais": payload.get("necessidadesEspeciais"),
            "status": "pendente",
        }

        await self.alta_provider.criar(nova_alta)
        return {"message": "Solicitação de alta registrada com sucesso."}

    async def atualizar_destino(self, alta_id: int, payload: dict, operador: str = "Sistema") -> dict:
        """Permite definir ou alterar o leito de destino e necessidades especiais."""
        alvo = await self.alta_provider.get_por_id(alta_id)
        if not alvo:
            raise HTTPException(status_code=404, detail="Solicitação de alta não encontrada.")

        dados = {}
        if "leitoDestino" in payload:
            dados["leito_destino"] = payload["leitoDestino"]
            dados["status"] = "definida"
            
            # Registra no histórico para gerar alerta automático
            if self.historico_provider:
                await self.historico_provider.registrar(
                    operador=operador,
                    tipo="alteracao_destino",
                    acao="Definiu destino de alta",
                    detalhes=f"Leito {alvo.lto_id}: Destino {payload['leitoDestino']}",
                    prontuario=str(alvo.prontuario)
                )

        if "necessidadesEspeciais" in payload:
            dados["necessidades_especiais"] = payload["necessidadesEspeciais"]

        await self.alta_provider.atualizar(alta_id, dados)
        return {"message": "Solicitação atualizada."}

    async def atualizar_destino_disponivel(self, alta_id: int, disponivel: bool, operador: str = "Sistema") -> dict:
        """Marca se o destino já está fisicamente disponível para o paciente."""
        alvo = await self.alta_provider.get_por_id(alta_id)
        if not alvo:
            raise HTTPException(status_code=404, detail="Solicitação de alta não encontrada.")

        await self.alta_provider.atualizar(alta_id, {"destino_disponivel": 1 if disponivel else 0})
        
        if disponivel and self.historico_provider:
             await self.historico_provider.registrar(
                operador=operador,
                tipo="destino_disponivel",
                acao="Destino Disponível",
                detalhes=f"Leito {alvo.lto_id}: Destino {alvo.leito_destino} está liberado.",
                prontuario=str(alvo.prontuario)
            )
        elif not disponivel and self.historico_provider:
             await self.historico_provider.registrar(
                operador=operador,
                tipo="destino_pendente",
                acao="Destino Indisponível",
                detalhes=f"Leito {alvo.lto_id}: Liberação do destino {alvo.leito_destino} foi CANCELADA.",
                prontuario=str(alvo.prontuario)
            )

        return {"message": "Status do destino atualizado."}

    async def cancelar_alta(self, alta_id: int) -> dict:
        """Cancela uma solicitação de alta ativa e limpa o estado do leito associado."""
        alvo = await self.alta_provider.get_por_id(alta_id)
        if not alvo:
            raise HTTPException(status_code=404, detail="Solicitação de alta não encontrada.")

        # Atualiza o status da solicitação para cancelada
        await self.alta_provider.atualizar(alta_id, {"status": "cancelada"})
        
        # Limpa o flag de alta solicitada no estado do leito associado
        if self.estado_provider:
            await self.estado_provider.salvar_alta(alvo.lto_id, False)

        return {"message": "Solicitação de alta cancelada."}
