from typing import List, Dict, Any, Optional
from fastapi import HTTPException
from providers.implementations.solicitacao_alta_provider import SolicitacaoAltaProvider

class AltasController:
    """
    Controller para gerenciar solicitações de alta da UTI.
    Combina dados do AGHU (para identificar o paciente no leito) com o estado local (SQLite).
    """

    def __init__(self, alta_provider: SolicitacaoAltaProvider, census_provider, estado_provider: Any = None):
        self.alta_provider = alta_provider
        self.census_provider = census_provider
        self.estado_provider = estado_provider

    async def listar_altas(self) -> List[Dict[str, Any]]:
        """Retorna todas as solicitações de alta (ativas), enriquecidas com dados do AGHU."""
        leitos_aghu = await self.census_provider.listar_leitos()
        leitos_map = {l["lto_lto_id"]: l for l in leitos_aghu}

        altas = await self.alta_provider.get_todas()
        resultado = []

        for alta in altas:
            # Filtra apenas as ativas para a listagem principal
            if alta.status not in ["pendente", "definida"]:
                continue

            leito_info = leitos_map.get(alta.lto_id, {})
            paciente_nome = leito_info.get("nome_paciente", "")
            especialidade = leito_info.get("especialidade_atual", "")

            resultado.append({
                "id": str(alta.id),
                "prontuario": alta.prontuario,
                "nomePaciente": paciente_nome,
                "especialidade": especialidade,
                "leitoAtual": alta.lto_id,
                "leitoDestino": alta.leito_destino or "Pendente (NIR)",
                "dataHora": alta.criado_em.strftime("%Y-%m-%d %H:%M") if alta.criado_em else "",
                "necessidadesEspeciais": alta.necessidades_especiais or "",
                "status": alta.status,
            })

        return resultado

    async def solicitar_alta(self, lto_id: str, payload: dict, operador: str = "Sistema") -> dict:
        """
        Registra o pedido de alta para um leito.
        Busca o paciente atual no AGHU e vincula à solicitação.
        """
        # Verifica se já existe uma solicitação ativa para o leito
        pendente = await self.alta_provider.get_por_lto_id(lto_id)
        if pendente:
            raise HTTPException(
                status_code=400,
                detail=f"Já existe uma solicitação de alta ativa para o leito {lto_id}."
            )

        # Identifica prontuário actual do paciente no AGHU
        leitos_aghu = await self.census_provider.listar_leitos()
        leito_info = next((l for l in leitos_aghu if l["lto_lto_id"] == lto_id), None)
        prontuario = str(leito_info["prontuario_atual"]) if leito_info and leito_info.get("prontuario_atual") else "N/D"

        nova_alta = {
            "lto_id": lto_id,
            "prontuario": prontuario,
            "leito_destino": payload.get("leitoDestino"),
            "necessidades_especiais": payload.get("necessidadesEspeciais"),
            "status": "pendente",
        }

        await self.alta_provider.criar(nova_alta)
        return {"message": "Solicitação de alta registrada com sucesso."}

    async def atualizar_destino(self, alta_id: int, payload: dict) -> dict:
        """Permite definir ou alterar o leito de destino e necessidades especiais."""
        alvo = await self.alta_provider.get_por_id(alta_id)
        if not alvo:
            raise HTTPException(status_code=404, detail="Solicitação de alta não encontrada.")

        dados = {}
        if "leitoDestino" in payload:
            dados["leito_destino"] = payload["leitoDestino"]
            dados["status"] = "definida"
        if "necessidadesEspeciais" in payload:
            dados["necessidades_especiais"] = payload["necessidadesEspeciais"]

        await self.alta_provider.atualizar(alta_id, dados)
        return {"message": "Solicitação atualizada."}

    async def cancelar_alta(self, alta_id: int) -> dict:
        """Cancela uma solicitação de alta ativa e limpa o estado do leito associado."""
        alvo = await self.alta_provider.get_por_id(alta_id)
        if not alvo:
            raise HTTPException(status_code=404, detail="Solicitação de alta não encontrada.")

        # Atualiza o status da solicitação para cancelada
        await self.alta_provider.atualizar(alta_id, {"status": "cancelada"})
        
        # Limpa o flag de alta solicitada no estado do leito associado
        if self.census_provider and self.alta_provider: # Ensure providers are initialized
            await self.census_provider.listar_leitos() # Refresh leitos data if needed for consistency
            # Find the leito_id from the cancelled alta record
            await self.estado_provider.salvar_alta(alvo.lto_id, False) # Assuming salvar_alta with False clears it

        return {"message": "Solicitação de alta cancelada."}
