from fastapi import APIRouter, Depends
from typing import Dict, Any, Optional
from auth.auth import auth_handler
from auth.roles import Role
from controllers.indicadores_controller import IndicadoresController
from dependencies import get_indicadores_controller, check_role

router = APIRouter(
    prefix="/api/indicadores",
    tags=["Indicadores"],
    dependencies=[
        Depends(auth_handler.decode_token)
    ],
)

@router.get("/resumo", response_model=Dict[str, Any])
async def obter_resumo_indicadores(
    data_inicio: Optional[str] = None,
    data_fim: Optional[str] = None,
    controller: IndicadoresController = Depends(get_indicadores_controller)
):
    """
    Retorna o JSON consolidado das métricas de ocupação e fluxo da UTI.
    """
    return await controller.obter_resumo(data_inicio, data_fim)
