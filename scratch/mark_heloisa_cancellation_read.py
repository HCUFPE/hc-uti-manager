import sys
import os
from sqlalchemy import select
from datetime import datetime

# Importar o gerenciador de banco de dados da aplicação
sys.path.insert(0, '/app/src')
from resources.database import DatabaseManager
from models.alerta import Alerta

async def run_mark():
    dsn = os.getenv("SQLITE_DSN") or "sqlite+aiosqlite:////app/data/app.db"
    db = DatabaseManager(dsn)
    
    async for session in db.get_session():
        print("Buscando alerta de exclusão de solicitação #59...")
        res = await session.execute(
            select(Alerta).where(
                Alerta.prontuario == "22307987",
                Alerta.titulo == "Solicitação para hoje removida"
            )
        )
        alertas = res.scalars().all()
        for a in alertas:
            print(f"Marcando ciente no alerta ID {a.id}...")
            a.lido = True
            a.lido_em = datetime.utcnow()
            a.lido_por = "Sistema"
            
        await session.commit()
        print("Ciente gravado com sucesso!")
        
    await db.close_connection()

if __name__ == "__main__":
    import asyncio
    asyncio.run(run_mark())
