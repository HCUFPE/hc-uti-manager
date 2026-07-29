import sys
import os
from sqlalchemy import select

sys.path.insert(0, '/app/src')
from resources.database import DatabaseManager
from models.alerta import Alerta

async def run():
    dsn = os.getenv("SQLITE_DSN") or "sqlite+aiosqlite:////app/data/app.db"
    db = DatabaseManager(dsn)
    
    async for session in db.get_session():
        res = await session.execute(select(Alerta).order_by(Alerta.id.desc()).limit(30))
        alertas = res.scalars().all()
        for a in alertas:
            print(f"ID: {a.id} | Titulo: {a.titulo} | Lido: {a.lido} | Pront: {a.prontuario} | Msg: {a.mensagem}")
            
if __name__ == '__main__':
    import asyncio
    asyncio.run(run())
