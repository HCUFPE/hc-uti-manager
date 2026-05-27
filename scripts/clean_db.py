import sys
import os
import asyncio
from dotenv import load_dotenv

# Adiciona o diretório 'src' ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

load_dotenv(os.path.abspath(os.path.join(os.path.dirname(__file__), '../.env')))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import delete

from models.alerta import Alerta
from models.historico_acao import HistoricoAcao
from models.solicitacao_alta import SolicitacaoAlta
from models.solicitacao_leito import SolicitacaoLeito
from models.leito_estado import LeitoEstado

async def clean_database():
    dsn = os.getenv("SQLITE_DSN")
    if not dsn:
        sqlite_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/app.db"))
        dsn = f"sqlite+aiosqlite:///{sqlite_path}"
    
    print(f"Connecting to database: {dsn}")
    engine = create_async_engine(dsn, echo=False)
    
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session() as session:
        print("Cleaning tables...")
        
        # Deletar de todas as tabelas especificadas
        deleted_alertas = await session.execute(delete(Alerta))
        deleted_historico = await session.execute(delete(HistoricoAcao))
        deleted_altas = await session.execute(delete(SolicitacaoAlta))
        deleted_solicitacoes = await session.execute(delete(SolicitacaoLeito))
        deleted_leito_estados = await session.execute(delete(LeitoEstado))
        
        await session.commit()
        
        print(f"Deleted {deleted_alertas.rowcount} alerts.")
        print(f"Deleted {deleted_historico.rowcount} history logs.")
        print(f"Deleted {deleted_altas.rowcount} alta requests.")
        print(f"Deleted {deleted_solicitacoes.rowcount} leito requests.")
        print(f"Deleted {deleted_leito_estados.rowcount} leito states.")
        print("Database cleanup completed successfully.")

if __name__ == "__main__":
    asyncio.run(clean_database())
