import asyncio
import os
import sys
from sqlalchemy import text
from dotenv import load_dotenv

# Garantir que o diretório src esteja no sys.path para importar DatabaseManager
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
load_dotenv(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env')))

from resources.database import DatabaseManager

async def main():
    # Obtém o DSN da variável de ambiente ou assume o padrão no container
    sqlite_dsn = os.getenv("SQLITE_DSN") or "sqlite+aiosqlite:////app/data/app.db"
    print(f"Conectando ao banco SQLite em: {sqlite_dsn}")
    
    app_db = DatabaseManager(sqlite_dsn)
    
    async with app_db.async_session_maker() as session:
        # 1. Remover os usuários de teste mockados
        print("Removendo usuários de teste padrão (admin, bloco, nir, uti)...")
        await session.execute(
            text("DELETE FROM usuarios_perfis WHERE username IN ('admin', 'bloco', 'nir', 'uti');")
        )
        
        # 2. Purgar tabelas de simulação/mock
        print("Limpando tabelas de solicitações, leitos e logs de simulação...")
        await session.execute(text("DELETE FROM solicitacoes_leito;"))
        await session.execute(text("DELETE FROM solicitacoes_alta;"))
        await session.execute(text("DELETE FROM leito_estados;"))
        await session.execute(text("DELETE FROM historico_acoes;"))
        await session.execute(text("DELETE FROM alertas;"))
        await session.execute(text("DELETE FROM refresh_tokens;"))
        
        await session.commit()
        print("Limpeza de dados de simulação concluída com sucesso!")

if __name__ == '__main__':
    asyncio.run(main())
