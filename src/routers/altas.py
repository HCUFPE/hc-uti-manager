from fastapi import APIRouter, Depends
from typing import List, Dict, Any
from controllers.altas_controller import AltasController
from dependencies import get_altas_controller

router = APIRouter(prefix="/api/altas", tags=["Altas"])


@router.get("", response_model=List[Dict[str, Any]])
async def listar_altas(
    controller: AltasController = Depends(get_altas_controller)
):
    """
    Retorna todas as solicitações de alta pendentes/definidas,
    enriquecidas com dados do paciente do AGHU.
    """
    return await controller.listar_altas()


@router.post("/{lto_id}")
async def solicitar_alta(
    lto_id: str,
    payload: dict = {},
    controller: AltasController = Depends(get_altas_controller)
):
    """Registra uma nova solicitação de alta para o leito especificado."""
    return await controller.solicitar_alta(lto_id, payload)


@router.put("/{alta_id}")
async def atualizar_destino(
    alta_id: int,
    payload: dict,
    controller: AltasController = Depends(get_altas_controller)
):
    """Atualiza o destino e/ou necessidades especiais de uma solicitação de alta."""
    return await controller.atualizar_destino(alta_id, payload)


@router.delete("/{alta_id}", status_code=204)
async def cancelar_alta(
    alta_id: int,
    controller: AltasController = Depends(get_altas_controller)
):
    """Cancela uma solicitação de alta."""
    await controller.cancelar_alta(alta_id)
