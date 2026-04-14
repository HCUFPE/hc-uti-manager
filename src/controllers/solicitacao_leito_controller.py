from typing import List, Dict, Any, Optional
from fastapi import HTTPException
from providers.implementations.solicitacao_leito_provider import SolicitacaoLeitoProvider
from providers.implementations.leito_estado_provider import LeitoEstadoProvider

class SolicitacaoLeitoController:
    """
    Controller para gerenciar solicitações de vaga/leito na UTI.
    """

    def __init__(self, leito_provider: SolicitacaoLeitoProvider, estado_provider: LeitoEstadoProvider | None = None):
        self.leito_provider = leito_provider
        self.estado_provider = estado_provider


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
                "destino": s.destino,
                "dataHora": s.criado_em.strftime("%Y-%m-%d %H:%M") if s.criado_em else "",
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
            "status": "Pendente",
        }

        if not all([nova_solicitacao["prontuario"], nova_solicitacao["idade"], nova_solicitacao["especialidade"]]):
             raise HTTPException(status_code=400, detail="Campos obrigatorios ausentes.")

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
