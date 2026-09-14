from datetime import datetime, timezone
from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy import text

from version import (
    VERSION,
    APP_NAME,
    SYSTEM_TITLE,
    LAST_UPDATE,
    ORGANIZATION,
    DEPARTMENT,
)

router = APIRouter(prefix="/api", tags=["Health & Monitoring"])


@router.get(
    "/health",
    summary="Health Check Endpoint",
    description="Verifica a saúde do servidor FastAPI, versão e conexões ativas com os bancos de dados.",
)
async def health_check(request: Request):
    """
    Retorna o estado de saúde da aplicação, versão e testa conexões de banco com 'SELECT 1'.
    Se algum banco essencial falhar, responde HTTP 503; se tudo estiver ok, responde HTTP 200.
    """
    db_status = {}
    is_healthy = True

    # 1. Checar banco principal / local (app_db)
    try:
        if hasattr(request.app.state, "app_db") and request.app.state.app_db:
            async with request.app.state.app_db.async_session_maker() as session:
                await session.execute(text("SELECT 1"))
            db_status["app_db"] = "connected"
        else:
            db_status["app_db"] = "not_initialized"
            is_healthy = False
    except Exception as e:
        db_status["app_db"] = f"error: {str(e)}"
        is_healthy = False

    # 2. Checar banco secundário (AGHU / PostgreSQL, se existir no projeto)
    if hasattr(request.app.state, "aghu_db") and request.app.state.aghu_db:
        try:
            async with request.app.state.aghu_db.async_session_maker() as session:
                await session.execute(text("SELECT 1"))
            db_status["aghu_postgres"] = "connected"
        except Exception as e:
            db_status["aghu_postgres"] = f"error: {str(e)}"
    else:
        db_status["aghu_postgres"] = "disabled_or_not_configured"

    response_payload = {
        "status": "healthy" if is_healthy else "unhealthy",
        "app_name": APP_NAME,
        "system_title": SYSTEM_TITLE,
        "version": VERSION,
        "last_update": LAST_UPDATE,
        "organization": ORGANIZATION,
        "department": DEPARTMENT,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "databases": db_status,
    }

    status_code = (
        status.HTTP_200_OK if is_healthy else status.HTTP_503_SERVICE_UNAVAILABLE
    )
    return JSONResponse(content=response_payload, status_code=status_code)
