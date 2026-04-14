from fastapi import APIRouter, Depends
from typing import Dict, Any
from controllers.indicadores_controller import IndicadoresController
from dependencies import get_indicadores_controller

router = APIRouter(prefix="/api/indicadores", tags=["Indicadores"])

@router.get("/resumo", response_model=Dict[str, Any])
async def obter_resumo_indicadores(
    controller: IndicadoresController = Depends(get_indicadores_controller)
):
    """
    Retorna o JSON consolidado das métricas de ocupação e fluxo da UTI.
    """
    return await controller.obter_resumo()
