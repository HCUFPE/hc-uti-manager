from fastapi import APIRouter, Depends
from typing import List, Dict, Any
from controllers.solicitacao_leito_controller import SolicitacaoLeitoController
from dependencies import get_solicitacao_leito_controller

router = APIRouter(prefix="/api/solicitacoes-leito", tags=["Solicitacoes Leito"])

@router.get("", response_model=List[Dict[str, Any]])
async def listar_solicitacoes(
    controller: SolicitacaoLeitoController = Depends(get_solicitacao_leito_controller)
):
    """Retorna todas as solicitações de leito ativas."""
    return await controller.listar_solicitacoes()

@router.post("")
async def criar_solicitacao(
    payload: dict,
    controller: SolicitacaoLeitoController = Depends(get_solicitacao_leito_controller)
):
    """Registra uma nova solicitação de leito."""
    return await controller.criar_solicitacao(payload)

@router.put("/{sol_id}")
async def atualizar_status(
    sol_id: int,
    payload: dict,
    controller: SolicitacaoLeitoController = Depends(get_solicitacao_leito_controller)
):
    """Atualiza o status ou o destino de uma solicitação."""
    return await controller.atualizar_status(sol_id, payload)

@router.delete("/{sol_id}", status_code=204)
async def cancelar_solicitacao(
    sol_id: int,
    controller: SolicitacaoLeitoController = Depends(get_solicitacao_leito_controller)
):
    """Cancela uma solicitação de leito."""
    await controller.cancelar_solicitacao(sol_id)

@router.post("/{sol_id}/reservar")
async def reservar_leito(
    sol_id: int,
    payload: dict,
    controller: SolicitacaoLeitoController = Depends(get_solicitacao_leito_controller)
):
    """
    Reserva um leito para uma solicitação pendente.
    Payload: {"leito_id": "0502A"}
    """
    leito_id = payload.get("leito_id")
    return await controller.reservar_leito(sol_id, leito_id)
