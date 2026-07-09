# versao para 09/07/2026 as 13:42h
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
from models.historico_acao import HistoricoAcao
from models.usuario_perfil import UsuarioPerfil
from models.historico_ocupacao import HistoricoOcupacao

async def preencher_dias_passados_semana_atual(app):
    from datetime import date, timedelta
    from sqlalchemy import select
    from models.historico_ocupacao import HistoricoOcupacao
    from providers.implementations.banco_aghu.leito_aghu_provider import LeitoAghuProvider

    try:
        # Calcular os dias da semana atual até hoje
        hoje = date.today()
        # Segunda-feira da semana atual:
        segunda = hoje - timedelta(days=hoje.weekday())
        
        dias_a_checar = []
        d = segunda
        while d < hoje:
            dias_a_checar.append(d)
            d += timedelta(days=1)
            
        if not dias_a_checar:
            return
            
        async with app.state.app_db.async_session_maker() as app_session:
            stmt = select(HistoricoOcupacao).where(HistoricoOcupacao.data.in_(dias_a_checar))
            res = await app_session.execute(stmt)
            existentes = {rec.data for rec in res.scalars().all()}
            
            dias_faltantes = [d for d in dias_a_checar if d not in existentes]
            if dias_faltantes:
                print(f"Dias faltantes da semana atual encontrados: {dias_faltantes}. Preenchendo com a taxa atual...")
                # Calcula taxa atual
                async with app.state.aghu_db.async_session_maker() as aghu_session:
                    census_provider = LeitoAghuProvider(aghu_session)
                    leitos = await census_provider.listar_leitos()
                    total_leitos = len(leitos)
                    ocupados = [l for l in leitos if str(l.get("status") or "").upper() == "OCUPADO"]
                    total_ocupados = len(ocupados)
                    taxa = (total_ocupados / total_leitos * 100) if total_leitos > 0 else 0.0
                    
                for d_faltante in dias_faltantes:
                    new_rec = HistoricoOcupacao(data=d_faltante, taxa_ocupacao=taxa)
                    app_session.add(new_rec)
                await app_session.commit()
                print(f"Preenchimento retroativo de {len(dias_faltantes)} dias com taxa {taxa:.1f}% concluído!")
    except Exception as e:
        print(f"Erro ao preencher dias passados: {e}")

async def gravar_fechamento_diario(app):
    import asyncio
    from datetime import datetime, timedelta
    from sqlalchemy import select, text
    from providers.implementations.banco_aghu.leito_aghu_provider import LeitoAghuProvider
    from models.historico_ocupacao import HistoricoOcupacao
    
    print("Iniciando background task de histórico de ocupação...")
    
    while True:
        try:
            agora = datetime.now()
            # Fuso de Brasília local. Agendar fechamento para 23:59:00
            proximo_fechamento = datetime.combine(agora.date(), datetime.min.time().replace(hour=23, minute=59, second=0))
            if agora >= proximo_fechamento:
                proximo_fechamento += timedelta(days=1)
                
            sleep_seconds = (proximo_fechamento - agora).total_seconds()
            print(f"Próxima gravação da ocupação agendada para: {proximo_fechamento} (daqui a {sleep_seconds:.1f} segundos)")
            
            await asyncio.sleep(min(sleep_seconds, 600.0))
            
            agora_reavaliado = datetime.now()
            if agora_reavaliado < proximo_fechamento - timedelta(seconds=5):
                continue
                
            data_fechamento = proximo_fechamento.date()
            print(f"Executando fechamento diário de ocupação para a data: {data_fechamento}...")
            
            async with app.state.aghu_db.async_session_maker() as aghu_session:
                census_provider = LeitoAghuProvider(aghu_session)
                leitos = await census_provider.listar_leitos()
                total_leitos = len(leitos)
                ocupados = [l for l in leitos if str(l.get("status") or "").upper() == "OCUPADO"]
                total_ocupados = len(ocupados)
                taxa = (total_ocupados / total_leitos * 100) if total_leitos > 0 else 0.0
                
            async with app.state.app_db.async_session_maker() as app_session:
                stmt = select(HistoricoOcupacao).where(HistoricoOcupacao.data == data_fechamento)
                res = await app_session.execute(stmt)
                existing = res.scalar_one_or_none()
                if existing:
                    existing.taxa_ocupacao = taxa
                else:
                    new_rec = HistoricoOcupacao(data=data_fechamento, taxa_ocupacao=taxa)
                    app_session.add(new_rec)
                await app_session.commit()
                print(f"Taxa de ocupação de {taxa:.1f}% gravada com sucesso para {data_fechamento}!")
                
            await asyncio.sleep(65.0)
            
        except Exception as e:
            print(f"Erro na background task de ocupação: {e}")
            await asyncio.sleep(60.0)

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
    from sqlalchemy import text
    async with app.state.app_db.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        for col in ["cirurgia_finalizada_em", "encaminhamento_liberado_em"]:
            try:
                await conn.execute(text(f"ALTER TABLE solicitacoes_leito ADD COLUMN {col} DATETIME;"))
            except Exception:
                pass # Coluna já existe
    print("App SQLite tables checked/created.")

    import asyncio
    await preencher_dias_passados_semana_atual(app)
    asyncio.create_task(gravar_fechamento_diario(app))

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
    title="HC-UTI Manager",
    description="Aplicação Backend monolítica (API REST) em Python/FastAPI.",
    version="1.0.0",
    lifespan=lifespan,
)

# Placeholder para incluir os roteadores da API
from routers import paciente, auth, admin, leito, altas, solicitacoes_leito, alertas, indicadores, historico
app.include_router(paciente.router)
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(leito.router)
app.include_router(altas.router)
app.include_router(solicitacoes_leito.router)
app.include_router(alertas.router)
app.include_router(indicadores.router)
app.include_router(historico.router)

# Serve o frontend Vue 3 empacotado
static_dir = os.path.join(os.path.dirname(__file__), "static", "dist")
if os.path.isdir(static_dir):
    assets_dir = os.path.join(static_dir, "assets")
    if os.path.isdir(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        if full_path.startswith("api"):
             raise HTTPException(status_code=404, detail="API route not found")
        
        requested_file = os.path.join(static_dir, full_path)
        if full_path and os.path.isfile(requested_file):
            return FileResponse(requested_file)

        index_file = os.path.join(static_dir, "index.html")
        if os.path.exists(index_file):
            return FileResponse(index_file)
        
        raise HTTPException(status_code=404, detail="Index file not found")
else:
    print(f"WARNING: Static directory {static_dir} not found.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
