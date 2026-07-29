import sys
import os
from datetime import datetime

# Importar o gerenciador de banco de dados da aplicação
sys.path.insert(0, '/app/src')
from resources.database import DatabaseManager
from models.historico_acao import HistoricoAcao

async def invert_logs_timestamps():
    dsn = os.getenv("SQLITE_DSN") or "sqlite+aiosqlite:////app/data/app.db"
    db = DatabaseManager(dsn)
    
    async for session in db.get_session():
        from sqlalchemy import update
        
        # 1. Inverter Mariano -> Gisele (Colocar o cancelamento de reserva em 10:59:04.951300, que é 1s antes de 10:59:05)
        print("Invertendo ordem cronológica da troca Heloísa -> Gisele...")
        await session.execute(
            update(HistoricoAcao)
            .where(
                HistoricoAcao.prontuario == "21036074",
                HistoricoAcao.tipo == "cancelamento_solicitante",
                HistoricoAcao.detalhes.like("%13938907%")
            )
            .values(
                criado_em=datetime.fromisoformat("2026-07-29 10:59:04.951300")
            )
        )
        
        # 2. Inverter Damião -> José Carlos (Colocar o cancelamento de reserva em 17:27:18.905922, que é 1s antes de 17:27:19.905922)
        print("Invertendo ordem cronológica da troca Damião -> José Carlos...")
        await session.execute(
            update(HistoricoAcao)
            .where(
                HistoricoAcao.prontuario == "22064729",
                HistoricoAcao.tipo == "cancelamento_solicitante",
                HistoricoAcao.detalhes.like("%21931076%")
            )
            .values(
                criado_em=datetime.fromisoformat("2026-07-29 17:27:18.905922")
            )
        )
        
        await session.commit()
        print("Inversão cronológica concluída com sucesso!")
        
    await db.close_connection()

if __name__ == "__main__":
    import asyncio
    asyncio.run(invert_logs_timestamps())
