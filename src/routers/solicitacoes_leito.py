from fastapi import APIRouter, Depends
from typing import List, Dict, Any
from controllers.solicitacao_leito_controller import SolicitacaoLeitoController
from dependencies import get_solicitacao_leito_controller, get_historico_provider
from providers.implementations.historico_provider import HistoricoProvider
from auth.auth import auth_handler

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
    controller: SolicitacaoLeitoController = Depends(get_solicitacao_leito_controller),
    historico: HistoricoProvider = Depends(get_historico_provider),
    current_user: dict = Depends(auth_handler.decode_token),
):
    """Registra uma nova solicitação de leito."""
    result = await controller.criar_solicitacao(payload)
    prontuario = payload.get("prontuario", "")
    especialidade = payload.get("especialidade", "")
    tipo_sol = payload.get("tipo", "")
    await historico.registrar(
        operador=current_user.get("username", "Sistema"),
        tipo="solicitacao",
        acao="Nova solicitação de vaga",
        detalhes=f"Prontuário {prontuario} — {especialidade} ({tipo_sol})",
    )
    return result

@router.put("/{sol_id}")
async def atualizar_status(
    sol_id: int,
    payload: dict,
    controller: SolicitacaoLeitoController = Depends(get_solicitacao_leito_controller),
    historico: HistoricoProvider = Depends(get_historico_provider),
    current_user: dict = Depends(auth_handler.decode_token),
):
    """Atualiza o status ou o destino de uma solicitação."""
    result = await controller.atualizar_status(sol_id, payload)
    novo_status = payload.get("status", "")
    destino = payload.get("destino", "")
    detalhe = f"Solicitação #{sol_id}"
    if destino:
        detalhe += f" → {destino}"
    await historico.registrar(
        operador=current_user.get("username", "Sistema"),
        tipo="destino" if destino else "status",
        acao=f"Atualizou status para {novo_status}" if novo_status else "Definiu destino",
        detalhes=detalhe,
    )
    return result

@router.delete("/{sol_id}", status_code=204)
async def cancelar_solicitacao(
    sol_id: int,
    controller: SolicitacaoLeitoController = Depends(get_solicitacao_leito_controller),
    historico: HistoricoProvider = Depends(get_historico_provider),
    current_user: dict = Depends(auth_handler.decode_token),
):
    """Cancela uma solicitação de leito."""
    await controller.cancelar_solicitacao(sol_id)
    await historico.registrar(
        operador=current_user.get("username", "Sistema"),
        tipo="cancelamento",
        acao="Cancelou solicitação de vaga",
        detalhes=f"Solicitação #{sol_id}",
    )

@router.post("/{sol_id}/reservar")
async def reservar_leito(
    sol_id: int,
    payload: dict,
    controller: SolicitacaoLeitoController = Depends(get_solicitacao_leito_controller),
    historico: HistoricoProvider = Depends(get_historico_provider),
    current_user: dict = Depends(auth_handler.decode_token),
):
    """Reserva um leito para uma solicitação pendente.
    Payload: {"leito_id": "0502A"}
    """
    leito_id = payload.get("leito_id")
    result = await controller.reservar_leito(sol_id, leito_id)
    await historico.registrar(
        operador=current_user.get("username", "Sistema"),
        tipo="reserva",
        acao="Reservou leito para solicitação",
        detalhes=f"Solicitação #{sol_id} → Leito {leito_id}",
    )
    return result
