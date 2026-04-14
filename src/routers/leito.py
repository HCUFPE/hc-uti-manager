from fastapi import APIRouter, Depends, status
from controllers.leitos_controller import LeitosController
from models.reserva_leito import ReservaLeitoInput
from dependencies import get_leito_controller, get_solicitacao_leito_provider
from typing import List, Dict, Any, Optional
from providers.implementations.solicitacao_leito_provider import SolicitacaoLeitoProvider

router = APIRouter(prefix="/api/leitos", tags=["Leitos"])

@router.post("/{lto_lto_id}/reservar")
async def reservar_leito(
    lto_lto_id: str,
    payload: ReservaLeitoInput,
    controller: LeitosController = Depends(get_leito_controller)
):
    return await controller.reservar(lto_lto_id, payload)

@router.delete("/{leito_id}/reserva", status_code=status.HTTP_200_OK)
async def cancelar_reserva(
    leito_id: str,
    controller: LeitosController = Depends(get_leito_controller),
    solicitacao_provider: SolicitacaoLeitoProvider = Depends(get_solicitacao_leito_provider)
):
    return await controller.cancelar_reserva(leito_id, solicitacao_provider)

@router.post(
    "/{leito_id}/alta",
    status_code=status.HTTP_204_NO_CONTENT
)
async def solicitar_alta(
    leito_id: str,
    controller: LeitosController = Depends(get_leito_controller)
):
    await controller.solicitar_alta(leito_id)

@router.delete(
    "/{leito_id}/alta",
    status_code=status.HTTP_204_NO_CONTENT
)
async def cancelar_alta(
    leito_id: str,
    controller: LeitosController = Depends(get_leito_controller)
):
    await controller.cancelar_alta(leito_id) 

@router.get("", response_model=List[Dict[str, Any]])
async def listar_leitos(
    controller: LeitosController = Depends(get_leito_controller),
):
    """
    Retorna todos os leitos da unidade selecionada, com dados unificados do banco local e AGHU.
    """
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
        # Print to server logs and return trace for debugging (remove in production)
        print("ERROR in listar_leitos_disponiveis_para_reserva:\n", tb)
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail={"error": str(e), "trace": tb})