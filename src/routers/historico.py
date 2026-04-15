"""Router para consulta do Histórico de Ações."""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, Query

from auth.auth import auth_handler
from dependencies import get_historico_provider
from providers.implementations.historico_provider import HistoricoProvider

router = APIRouter(
    prefix="/api/historico",
    tags=["Histórico"],
    dependencies=[Depends(auth_handler.decode_token)],
)


@router.get("", response_model=List[Dict[str, Any]])
async def listar_historico(
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    tipo: Optional[str] = Query(default=None, description="Filtra por tipo: alta, reserva, cancelamento, solicitacao, destino, status"),
    operador: Optional[str] = Query(default=None),
    busca: Optional[str] = Query(default=None, description="Busca livre em ação, detalhes e operador"),
    provider: HistoricoProvider = Depends(get_historico_provider),
):
    """Retorna o histórico de ações do sistema, mais recentes primeiro."""
    return await provider.listar(
        limit=limit,
        offset=offset,
        tipo=tipo,
        operador=operador,
        busca=busca,
    )
