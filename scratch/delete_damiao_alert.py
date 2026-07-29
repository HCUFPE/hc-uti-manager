import sys
import os

# Importar o gerenciador de banco de dados da aplicação
sys.path.insert(0, '/app/src')
from resources.database import DatabaseManager
from models.alerta import Alerta

async def delete_damiao_alert():
    dsn = os.getenv("SQLITE_DSN") or "sqlite+aiosqlite:////app/data/app.db"
    db = DatabaseManager(dsn)
    
    async for session in db.get_session():
        from sqlalchemy import delete
        print("Deletando o alerta incorreto ID 341 do Damião...")
        await session.execute(
            delete(Alerta).where(Alerta.id == 341)
        )
        await session.commit()
        print("Alerta excluído com sucesso!")
        
    await db.close_connection()

if __name__ == "__main__":
    import asyncio
    asyncio.run(delete_damiao_alert())
