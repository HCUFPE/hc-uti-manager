from typing import List, Dict, Any, Optional
from datetime import timedelta
from fastapi import HTTPException
from providers.implementations.solicitacao_leito_provider import SolicitacaoLeitoProvider
from providers.implementations.leito_estado_provider import LeitoEstadoProvider
from providers.implementations.historico_provider import HistoricoProvider

class SolicitacaoLeitoController:
    """
    Controller para gerenciar solicitações de vaga/leito na UTI.
    """

    def __init__(
        self, 
        leito_provider: SolicitacaoLeitoProvider, 
        estado_provider: LeitoEstadoProvider | None = None,
        historico_provider: HistoricoProvider | None = None
    ):
        self.leito_provider = leito_provider
        self.estado_provider = estado_provider
        self.historico_provider = historico_provider

    async def _remanejar_prioridades(self, data_cirurgia: str, turno: str, prioridade_alvo: str, skip_id: int | None = None):
        """
        Lógica recursiva para empurrar prioridades: 
        Se eu definir algo como P1, quem era P1 vira P2, quem era P2 vira P3...
        """
        if not prioridade_alvo or prioridade_alvo not in ["P1", "P2", "P3", "P4", "P5"]:
            return

        # Busca se já existe alguém com essa mesma data, turno e prioridade
        todas = await self.leito_provider.get_todas()
        conflito = next((s for s in todas if s.data_cirurgia == data_cirurgia 
                         and s.turno == turno 
                         and s.prioridade == prioridade_alvo 
                         and s.id != skip_id), None)

        if conflito:
            # Define a próxima prioridade
            proxima = {
                "P1": "P2",
                "P2": "P3",
                "P3": "P4",
                "P4": "P5",
                "P5": None # P5 é o limite, ou vira nulo
            }.get(prioridade_alvo)

            # Primeiro remaneja quem está no caminho da próxima (recursão)
            if proxima:
                await self._remanejar_prioridades(data_cirurgia, turno, proxima, skip_id=conflito.id)
            
            # Depois atualiza o atual para a próxima
            await self.leito_provider.atualizar(conflito.id, {"prioridade": proxima})


    async def listar_solicitacoes(self) -> List[Dict[str, Any]]:
        """Retorna todas as solicitações de leito ativas."""
        solicitacoes = await self.leito_provider.get_todas()
        
        return [
            {
                "id": str(s.id),
                "prontuario": s.prontuario,
                "idade": s.idade,
                "especialidade": s.especialidade,
                "tipo": s.tipo,
                "status": s.status,
                "turno": s.turno,
                "data_cirurgia": s.data_cirurgia,
                "prioridade": s.prioridade,
                "perfil_solicitante": s.perfil_solicitante,
                "destino": s.destino,
                "dataHora": (s.criado_em - timedelta(hours=3)).strftime("%Y-%m-%d %H:%M") if s.criado_em else "",
            }
            for s in solicitacoes
        ]

    async def criar_solicitacao(self, payload: dict) -> dict:
        """Registra uma nova solicitação de leito."""
        nova_solicitacao = {
            "prontuario": payload.get("prontuario"),
            "idade": payload.get("idade"),
            "especialidade": payload.get("especialidade"),
            "tipo": payload.get("tipo"),
            "turno": payload.get("turno"),
            "data_cirurgia": payload.get("data_cirurgia"),
            "prioridade": payload.get("prioridade"),
            "status": "Pendente",
            "perfil_solicitante": payload.get("perfil_solicitante")
        }

        if not all([nova_solicitacao["prontuario"], nova_solicitacao["idade"], nova_solicitacao["especialidade"]]):
             raise HTTPException(status_code=400, detail="Campos obrigatorios ausentes.")

        # Remanejamento de prioridade antes de criar
        if nova_solicitacao["prioridade"] and nova_solicitacao["data_cirurgia"] and nova_solicitacao["turno"]:
            await self._remanejar_prioridades(nova_solicitacao["data_cirurgia"], nova_solicitacao["turno"], nova_solicitacao["prioridade"])

        await self.leito_provider.criar(nova_solicitacao)
        return {"message": "Solicitação de leito registrada com sucesso."}

    async def atualizar_status(self, sol_id: int, payload: dict) -> dict:
        """Atualiza o status ou o destino de uma solicitação."""
        alvo = await self.leito_provider.get_por_id(sol_id)
        if not alvo:
            raise HTTPException(status_code=404, detail="Solicitação não encontrada.")

        dados = {}
        if "status" in payload:
            dados["status"] = payload["status"]
        if "destino" in payload:
            dados["destino"] = payload["destino"]
            if payload.get("status") is None:
                dados["status"] = "Reservado"

        await self.leito_provider.atualizar(sol_id, dados)
        return {"message": "Solicitação atualizada."}

    async def editar_solicitacao(self, sol_id: int, payload: dict) -> dict:
        """
        Permite editar os dados de uma solicitação, 
        desde que ela ainda não tenha sido reservada.
        """
        alvo = await self.leito_provider.get_por_id(sol_id)
        if not alvo:
            raise HTTPException(status_code=404, detail="Solicitação não encontrada.")
            
        if alvo.status != "Pendente":
            raise HTTPException(
                status_code=403, 
                detail=f"Não é possível editar uma solicitação com status '{alvo.status}'. Cancele a reserva primeiro."
            )

        # Campos que podem ser editados
        campos_validos = ["prontuario", "idade", "especialidade", "tipo", "turno", "data_cirurgia", "prioridade"]
        dados_atualizar = {k: v for k, v in payload.items() if k in campos_validos}
        
        if not dados_atualizar:
            raise HTTPException(status_code=400, detail="Nenhum campo válido para atualização fornecido.")

        # Validação de campos obrigatórios (não podem ser vazios se fornecidos)
        campos_obrigatorios = ["prontuario", "idade", "especialidade", "tipo", "data_cirurgia", "turno"]
        for campo in campos_obrigatorios:
            valor = dados_atualizar.get(campo)
            if campo in dados_atualizar and (valor is None or str(valor).strip() == ""):
                raise HTTPException(status_code=400, detail=f"O campo '{campo}' é obrigatório e não pode ficar vazio.")

        # Se mudou prioridade, data ou turno, precisa remanejar
        prio = dados_atualizar.get("prioridade", alvo.prioridade)
        dt = dados_atualizar.get("data_cirurgia", alvo.data_cirurgia)
        trn = dados_atualizar.get("turno", alvo.turno)
        
        if prio and dt and trn and (prio != alvo.prioridade or dt != alvo.data_cirurgia or trn != alvo.turno):
            await self._remanejar_prioridades(dt, trn, prio, skip_id=sol_id)

        await self.leito_provider.atualizar(sol_id, dados_atualizar)
        return {"message": "Solicitação editada com sucesso."}

    async def cancelar_solicitacao(self, sol_id: int) -> dict:
        """Cancela uma solicitação de leito."""
        sucesso = await self.leito_provider.deletar(sol_id)
        if not sucesso:
            raise HTTPException(status_code=404, detail="Solicitação não encontrada.")
            
        return {"message": "Solicitação cancelada."}

    async def reservar_leito(self, sol_id: int, leito_id: str) -> dict:
        """
        Vincula uma solicitação pendente a um leito específico,
        criando uma reserva no estado local do leito.
        """
        solicitacao = await self.leito_provider.get_por_id(sol_id)
        if not solicitacao:
            raise HTTPException(status_code=404, detail="Solicitação não encontrada.")
            
        if not self.estado_provider:
            raise HTTPException(status_code=500, detail="Estado provider não configurado.")

        # 1. Registrar a reserva no estado local do leito
        await self.estado_provider.salvar_reserva(
            lto_id=leito_id,
            prontuario=int(solicitacao.prontuario),
            idade=solicitacao.idade,
            especialidade=solicitacao.especialidade,
            solicitacao_id=solicitacao.id
        )

        # 2. Atualizar a solicitação original
        await self.leito_provider.atualizar(sol_id, {
            "status": "Reservado",
            "destino": f"Leito {leito_id}"
        })

        return {"message": f"Reserva do leito {leito_id} realizada com sucesso."}

    async def cancelar_reserva(self, sol_id: int) -> dict:
        """
        Remove o vínculo entre a solicitação e o leito, 
        voltando o status para 'Pendente'.
        """
        solicitacao = await self.leito_provider.get_por_id(sol_id)
        if not solicitacao:
            raise HTTPException(status_code=404, detail="Solicitação não encontrada.")

        if not self.estado_provider:
            raise HTTPException(status_code=500, detail="Estado provider não configurado.")

        # 1. Limpar a reserva no leito (SQLite)
        await self.estado_provider.limpar_reserva_por_solicitacao(sol_id)

        # 2. Voltar a solicitação para Pendente (Postgres/SQLite principal)
        await self.leito_provider.atualizar(sol_id, {
            "status": "Pendente",
            "destino": None
        })

        return {"message": "Reserva cancelada. Solicitação voltou para Pendente."}
