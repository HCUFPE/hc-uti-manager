from fastapi import APIRouter, Depends, status, HTTPException, Query
from auth.roles import Role
from controllers.leitos_controller import LeitosController
from models.reserva_leito import ReservaLeitoInput
from dependencies import get_leito_controller, get_solicitacao_leito_provider, get_historico_provider, check_role
from typing import List, Dict, Any, Optional
from providers.implementations.solicitacao_leito_provider import SolicitacaoLeitoProvider
from providers.implementations.historico_provider import HistoricoProvider
from auth.auth import auth_handler

router = APIRouter(prefix="/api/leitos", tags=["Leitos"])

@router.post("/{lto_lto_id}/reservar")
async def reservar_leito(
    lto_lto_id: str,
    payload: ReservaLeitoInput,
    controller: LeitosController = Depends(get_leito_controller),
    historico: HistoricoProvider = Depends(get_historico_provider),
    current_user: dict = Depends(check_role([Role.ADMIN, Role.UTI, Role.UTI_ADMIN])),
):
    result = await controller.reservar(lto_lto_id, payload)
    await historico.registrar(
        operador=current_user.get("username", "Sistema"),
        tipo="reserva",
        acao="Reservou leito",
        detalhes=f"Leito {lto_lto_id} para prontuário {payload.prontuario}",
        prontuario=str(payload.prontuario)
    )
    return result

@router.delete("/{leito_id}/reserva", status_code=status.HTTP_200_OK)
async def cancelar_reserva(
    leito_id: str,
    motivo: str = Query(..., description="Motivo do cancelamento da reserva"),
    controller: LeitosController = Depends(get_leito_controller),
    solicitacao_provider: SolicitacaoLeitoProvider = Depends(get_solicitacao_leito_provider),
    historico: HistoricoProvider = Depends(get_historico_provider),
    current_user: dict = Depends(check_role([Role.ADMIN, Role.UTI, Role.UTI_ADMIN])),
):
    result = await controller.cancelar_reserva(leito_id, solicitacao_provider)
    solicitacao = result.get("solicitacao")
    prontuario_reserva = result.get("prontuario")
    
    detalhes = f"Leito {leito_id}"
    prontuario_log = None

    if solicitacao:
        prontuario_log = str(solicitacao.prontuario)
        detalhes = f"Solicitação #{solicitacao.id} (Prontuário {prontuario_log}) voltou para Pendente (Leito {leito_id} liberado)"
    elif prontuario_reserva:
        prontuario_log = str(prontuario_reserva)
        detalhes = f"Reserva manual do Prontuário {prontuario_log} cancelada (Leito {leito_id} liberado)"

    if motivo:
        detalhes += f" - Motivo: {motivo}"

    await historico.registrar(
        operador=current_user.get("username", "Sistema"),
        tipo="cancelamento_reserva",
        acao="Cancelou reserva",
        detalhes=detalhes,
        prontuario=prontuario_log
    )
    return result

@router.post(
    "/{leito_id}/alta",
    status_code=status.HTTP_204_NO_CONTENT
)
async def solicitar_alta(
    leito_id: str,
    controller: LeitosController = Depends(get_leito_controller),
    historico: HistoricoProvider = Depends(get_historico_provider),
    current_user: dict = Depends(check_role([Role.ADMIN, Role.UTI, Role.UTI_ADMIN])),
):
    await controller.solicitar_alta(leito_id)
    # Busca o prontuário para o histórico (similar ao que o controller faz)
    leitos_censo = await controller.census_provider.listar_leitos()
    leito_info = next((l for l in leitos_censo if l['lto_lto_id'] == leito_id), None)
    prontuario = str(leito_info['prontuario_atual']) if leito_info and leito_info.get('prontuario_atual') else None

    await historico.registrar(
        operador=current_user.get("username", "Sistema"),
        tipo="alta",
        acao="Solicitou alta",
        detalhes=f"Leito {leito_id}",
        prontuario=prontuario
    )

@router.delete(
    "/{leito_id}/alta",
    status_code=status.HTTP_204_NO_CONTENT
)
async def cancelar_alta(
    leito_id: str,
    controller: LeitosController = Depends(get_leito_controller),
    historico: HistoricoProvider = Depends(get_historico_provider),
    current_user: dict = Depends(check_role([Role.ADMIN, Role.UTI, Role.UTI_ADMIN])),
):
    # Busca o prontuário para o histórico antes do cancelamento
    leitos_censo = await controller.census_provider.listar_leitos()
    leito_info = next((l for l in leitos_censo if l['lto_lto_id'] == leito_id), None)
    prontuario = str(leito_info['prontuario_atual']) if leito_info and leito_info.get('prontuario_atual') else None

    await controller.cancelar_alta(leito_id)
    await historico.registrar(
        operador=current_user.get("username", "Sistema"),
        tipo="cancelamento",
        acao="Cancelou alta",
        detalhes=f"Leito {leito_id}",
        prontuario=prontuario
    )

@router.get("", response_model=List[Dict[str, Any]])
async def listar_leitos(
    controller: LeitosController = Depends(get_leito_controller),
):
    """Retorna todos os leitos da unidade selecionada, com dados unificados do banco local e AGHU."""
    return await controller.listar_leitos()

@router.get("/disponiveis")
async def listar_leitos_disponiveis_para_reserva(
    incluir_reservados: bool = Query(False, description="Incluir leitos com reserva ativa na listagem"),
    controller: LeitosController = Depends(get_leito_controller)
):
    return await controller.listar_leitos_disponiveis_para_reserva(incluir_reservados=incluir_reservados)