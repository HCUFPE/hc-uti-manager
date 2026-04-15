from fastapi import APIRouter, Depends
from typing import List, Dict, Any
from controllers.altas_controller import AltasController
from dependencies import get_altas_controller, get_historico_provider
from providers.implementations.historico_provider import HistoricoProvider
from auth.auth import auth_handler

router = APIRouter(prefix="/api/altas", tags=["Altas"])


@router.get("", response_model=List[Dict[str, Any]])
async def listar_altas(
    controller: AltasController = Depends(get_altas_controller)
):
    """Retorna todas as solicitações de alta pendentes/definidas,
    enriquecidas com dados do paciente do AGHU."""
    return await controller.listar_altas()


@router.post("/{lto_id}")
async def solicitar_alta(
    lto_id: str,
    payload: dict = {},
    controller: AltasController = Depends(get_altas_controller),
    historico: HistoricoProvider = Depends(get_historico_provider),
    current_user: dict = Depends(auth_handler.decode_token),
):
    """Registra uma nova solicitação de alta para o leito especificado."""
    result = await controller.solicitar_alta(lto_id, payload)
    await historico.registrar(
        operador=current_user.get("username", "Sistema"),
        tipo="alta",
        acao="Solicitou alta",
        detalhes=f"Leito {lto_id}",
    )
    return result


@router.put("/{alta_id}")
async def atualizar_destino(
    alta_id: int,
    payload: dict,
    controller: AltasController = Depends(get_altas_controller),
    historico: HistoricoProvider = Depends(get_historico_provider),
    current_user: dict = Depends(auth_handler.decode_token),
):
    """Atualiza o destino e/ou necessidades especiais de uma solicitação de alta."""
    result = await controller.atualizar_destino(alta_id, payload)
    destino = payload.get("leitoDestino", "")
    await historico.registrar(
        operador=current_user.get("username", "Sistema"),
        tipo="destino",
        acao="Definiu destino de alta",
        detalhes=f"Alta #{alta_id} → {destino}" if destino else f"Alta #{alta_id} atualizada",
    )
    return result


@router.delete("/{alta_id}", status_code=204)
async def cancelar_alta(
    alta_id: int,
    controller: AltasController = Depends(get_altas_controller),
    historico: HistoricoProvider = Depends(get_historico_provider),
    current_user: dict = Depends(auth_handler.decode_token),
):
    """Cancela uma solicitação de alta."""
    await controller.cancelar_alta(alta_id)
    await historico.registrar(
        operador=current_user.get("username", "Sistema"),
        tipo="cancelamento",
        acao="Cancelou solicitação de alta",
        detalhes=f"Alta #{alta_id}",
    )
