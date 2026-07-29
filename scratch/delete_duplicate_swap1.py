import sys
import os
from sqlalchemy import delete

# Importar o gerenciador de banco de dados da aplicação
sys.path.insert(0, '/app/src')
from resources.database import DatabaseManager
from models.alerta import Alerta

async def delete_duplicate():
    dsn = os.getenv("SQLITE_DSN") or "sqlite+aiosqlite:////app/data/app.db"
    db = DatabaseManager(dsn)
    
    async for session in db.get_session():
        # Deletar especificamente o alerta ID 327
        print("Deletando alerta duplicado ID 327...")
        await session.execute(
            delete(Alerta).where(Alerta.id == 327)
        )
        await session.commit()
        print("Alerta duplicado removido com sucesso!")
        
    await db.close_connection()

if __name__ == "__main__":
    import asyncio
    asyncio.run(delete_duplicate())
