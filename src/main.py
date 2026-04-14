from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
import os
import sys
# Ensure local package modules (e.g., `models`, `controllers`) are importable when running
# the app with uvicorn from the project root. This inserts `src/` into sys.path.
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from contextlib import asynccontextmanager
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

from resources.database import DatabaseManager, Base
# Importar modelos para garantir que sejam registrados no metadata
from models.refresh_token import RefreshToken
from models.leito_estado import LeitoEstado
from models.solicitacao_alta import SolicitacaoAlta
from models.solicitacao_leito import SolicitacaoLeito

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting up...")

    # Initialize AGHU DB Manager and store in app.state
    aghu_dsn = os.getenv("POSTGRES_DSN")
    if aghu_dsn:
        app.state.aghu_db = DatabaseManager(aghu_dsn)
        print("AGHU PostgreSQL connection pool initialized.")
    else:
        print("WARNING: POSTGRES_DSN not found. Skipping AGHU DB initialization.")

    # Initialize App DB Manager (SQLite) and store in app.state
    app_dsn = os.getenv("SQLITE_DSN")
    sqlite_path = os.getenv("SQLITE_PATH")
    if not app_dsn and sqlite_path:
        app_dsn = f"sqlite+aiosqlite:///{os.path.abspath(sqlite_path)}"
        print(f"INFO: Derived SQLITE_DSN from SQLITE_PATH={sqlite_path}")
    if not app_dsn:
        default_sqlite_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "app.db"))
        app_dsn = f"sqlite+aiosqlite:///{default_sqlite_path}"
        print(f"WARNING: SQLITE_DSN not found. Using default local SQLite at {default_sqlite_path}.")
    app.state.app_db = DatabaseManager(app_dsn)
    print("App SQLite connection pool initialized.")

    # Create tables for App DB (if they don't exist) - for development only, Alembic handles this in production
    async with app.state.app_db.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("App SQLite tables checked/created.")

    yield

    # Shutdown
    print("Shutting down...")
    if hasattr(app.state, 'aghu_db') and app.state.aghu_db:
        await app.state.aghu_db.close_connection()
        print("AGHU PostgreSQL connection pool closed.")
    if hasattr(app.state, 'app_db') and app.state.app_db:
        await app.state.app_db.close_connection()
        print("App SQLite connection pool closed.")

app = FastAPI(
    title="Esqueleto de Aplicação Web Full-Stack",
    description="Aplicação Backend monolítica (API REST) em Python/FastAPI, com foco em acesso e agregação de dados heterogêneos.",
    version="1.0.0",
    lifespan=lifespan,
)

# Placeholder para incluir os roteadores da API
from routers import paciente, auth, admin, leito, altas, solicitacoes_leito, alertas, indicadores
app.include_router(paciente.router)
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(leito.router)
app.include_router(altas.router)
app.include_router(solicitacoes_leito.router)
app.include_router(alertas.router)
app.include_router(indicadores.router)

# Exemplo:
# from .routers import aih, bpa, material
# app.include_router(aih.router)
# app.include_router(bpa.router)
# app.include_router(material.router)

# Serve o frontend Vue 3 empacotado (DEVE ficar DEPOIS dos routers,
# pois app.mount("/") captura todas as requisições não atendidas acima)
static_dir = os.path.join(os.path.dirname(__file__), "static", "dist")
if os.path.isdir(static_dir):
    app.mount("/assets", StaticFiles(directory=os.path.join(static_dir, "assets")), name="assets")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        # Se o caminho for uma API, deixa que o FastAPI retorne 404 normal se não existir
        if full_path.startswith("api"):
             raise HTTPException(status_code=404, detail="API route not found")
        
        index_file = os.path.join(static_dir, "index.html")
        if os.path.exists(index_file):
            return FileResponse(index_file)
        raise HTTPException(status_code=404, detail="Index file not found")
else:
    print(f"WARNING: Static directory {static_dir} not found.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
