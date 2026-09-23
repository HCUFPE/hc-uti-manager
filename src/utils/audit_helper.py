import json
import logging
from typing import Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from models.audit_log import AuditLog, CategoriaAuditoria

logger = logging.getLogger(__name__)

async def registrar_auditoria(
    session: AsyncSession,
    categoria: str,
    acao: str,
    usuario_id: Optional[str] = None,
    detalhes: Optional[str] = None,
    estado_anterior: Optional[Any] = None,
    estado_novo: Optional[Any] = None
) -> None:
    """
    Grava um log de auditoria imutável no banco de dados.
    """
    try:
        str_anterior = json.dumps(estado_anterior, ensure_ascii=False) if estado_anterior is not None else None
        str_novo = json.dumps(estado_novo, ensure_ascii=False) if estado_novo is not None else None

        log_entry = AuditLog(
            categoria=categoria,
            acao=acao,
            usuario_id=usuario_id,
            detalhes=detalhes,
            estado_anterior=str_anterior,
            estado_novo=str_novo
        )
        session.add(log_entry)
        await session.commit()
    except Exception as e:
        logger.error(f"Erro ao gravar log de auditoria: {e}")
