import sys
import os
from sqlalchemy import select, delete
from datetime import datetime

# Importar o gerenciador de banco de dados da aplicação
sys.path.insert(0, '/app/src')
from resources.database import DatabaseManager
from models.alerta import Alerta

async def fix_swap2():
    dsn = os.getenv("SQLITE_DSN") or "sqlite+aiosqlite:////app/data/app.db"
    db = DatabaseManager(dsn)
    
    async for session in db.get_session():
        # 1. Deletar o alerta ID 329 (Vaga Reservada pela UTI redundante)
        print("Deletando alerta redundante ID 329...")
        await session.execute(
            delete(Alerta).where(Alerta.id == 329)
        )
        
        # 2. Ajustar o horário de criação do alerta único ID 328 para 07:59 (10:59 UTC)
        print("Buscando alerta ID 328 para ajustar data/hora...")
        res = await session.execute(
            select(Alerta).where(Alerta.id == 328)
        )
        alerta_328 = res.scalar_one_or_none()
        if alerta_328:
            exact_time = datetime.fromisoformat("2026-07-29 10:59:05.951300")
            alerta_328.criado_em = exact_time
            alerta_328.lido_em = exact_time
            print("Alerta ID 328 atualizado com a hora correta: 07:59.")
            
        await session.commit()
        print("Ajuste da segunda troca concluído!")
        
    await db.close_connection()

if __name__ == "__main__":
    import asyncio
    asyncio.run(fix_swap2())
