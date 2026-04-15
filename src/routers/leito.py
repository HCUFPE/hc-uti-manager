from fastapi import APIRouter, Depends, status
from controllers.leitos_controller import LeitosController
from models.reserva_leito import ReservaLeitoInput
from dependencies import get_leito_controller, get_solicitacao_leito_provider, get_historico_provider
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
    current_user: dict = Depends(auth_handler.decode_token),
):
    result = await controller.reservar(lto_lto_id, payload)
    await historico.registrar(
        operador=current_user.get("username", "Sistema"),
        tipo="reserva",
        acao="Reservou leito",
        detalhes=f"Leito {lto_lto_id} para prontuário {payload.prontuario}",
    )
    return result

@router.delete("/{leito_id}/reserva", status_code=status.HTTP_200_OK)
async def cancelar_reserva(
    leito_id: str,
    controller: LeitosController = Depends(get_leito_controller),
    solicitacao_provider: SolicitacaoLeitoProvider = Depends(get_solicitacao_leito_provider),
    historico: HistoricoProvider = Depends(get_historico_provider),
    current_user: dict = Depends(auth_handler.decode_token),
):
    result = await controller.cancelar_reserva(leito_id, solicitacao_provider)
    await historico.registrar(
        operador=current_user.get("username", "Sistema"),
        tipo="cancelamento",
        acao="Cancelou reserva",
        detalhes=f"Leito {leito_id}",
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
    current_user: dict = Depends(auth_handler.decode_token),
):
    await controller.solicitar_alta(leito_id)
    await historico.registrar(
        operador=current_user.get("username", "Sistema"),
        tipo="alta",
        acao="Solicitou alta",
        detalhes=f"Leito {leito_id}",
    )

@router.delete(
    "/{leito_id}/alta",
    status_code=status.HTTP_204_NO_CONTENT
)
async def cancelar_alta(
    leito_id: str,
    controller: LeitosController = Depends(get_leito_controller),
    historico: HistoricoProvider = Depends(get_historico_provider),
    current_user: dict = Depends(auth_handler.decode_token),
):
    await controller.cancelar_alta(leito_id)
    await historico.registrar(
        operador=current_user.get("username", "Sistema"),
        tipo="cancelamento",
        acao="Cancelou alta",
        detalhes=f"Leito {leito_id}",
    )

@router.get("", response_model=List[Dict[str, Any]])
async def listar_leitos(
    controller: LeitosController = Depends(get_leito_controller),
):
    """Retorna todos os leitos da unidade selecionada, com dados unificados do banco local e AGHU."""
    return await controller.listar_leitos()

@router.get("/disponiveis-para-reserva")
async def listar_leitos_disponiveis_para_reserva(
    controller: LeitosController = Depends(get_leito_controller)
):
    try:
        return await controller.listar_leitos_disponiveis_para_reserva()
    except Exception as e:
        import traceback
        tb = traceback.format_exc()
        print("ERROR in listar_leitos_disponiveis_para_reserva:\n", tb)
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail={"error": str(e), "trace": tb})