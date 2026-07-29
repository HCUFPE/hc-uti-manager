import sys
import os
from sqlalchemy import select
from datetime import datetime

# Importar o gerenciador de banco de dados da aplicação
sys.path.insert(0, '/app/src')
from resources.database import DatabaseManager
from models.alerta import Alerta

async def run():
    dsn = os.getenv("SQLITE_DSN") or "sqlite+aiosqlite:////app/data/app.db"
    db = DatabaseManager(dsn)
    
    async for session in db.get_session():
        # Consultar alertas criados a partir de 2026-07-29 (UTC)
        res = await session.execute(
            select(Alerta).where(Alerta.criado_em >= datetime(2026, 7, 29)).order_by(Alerta.id.asc())
        )
        alertas = res.scalars().all()
        for a in alertas:
            # Converter UTC para Brasília (-3h) apenas para visualização
            criado_local = a.criado_em - timedelta(hours=3) if a.criado_em else None
            t_str = criado_local.strftime("%H:%M:%S") if criado_local else "N/D"
            print(f"ID: {a.id} | Hora: {t_str} | Titulo: {a.titulo} | Lido: {a.lido} ({a.lido_por}) | Pront: {a.prontuario} | Msg: {a.mensagem}")
            
if __name__ == '__main__':
    from datetime import timedelta
    import asyncio
    asyncio.run(run())
