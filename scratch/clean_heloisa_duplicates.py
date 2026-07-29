import sys
import os

# Importar o gerenciador de banco de dados da aplicação
sys.path.insert(0, '/app/src')
from resources.database import DatabaseManager
from models.alerta import Alerta
from models.historico_acao import HistoricoAcao

async def clean_heloisa_duplicates():
    dsn = os.getenv("SQLITE_DSN") or "sqlite+aiosqlite:////app/data/app.db"
    db = DatabaseManager(dsn)
    
    async for session in db.get_session():
        from sqlalchemy import delete
        
        # 1. Deletar o alerta incorreto ID 328
        print("Deletando o alerta incorreto ID 328...")
        await session.execute(
            delete(Alerta).where(Alerta.id == 328)
        )
        
        # 2. Deletar o registro de histórico incorreto que gerou o ID 328
        print("Deletando log incorreto do histórico...")
        await session.execute(
            delete(HistoricoAcao).where(
                HistoricoAcao.prontuario == "21036074",
                HistoricoAcao.tipo == "cancelamento_solicitante",
                HistoricoAcao.detalhes.like("%voltou para Pendente%")
            )
        )
        
        await session.commit()
        print("Limpeza de duplicidade concluída!")
        
    await db.close_connection()

if __name__ == "__main__":
    import asyncio
    asyncio.run(clean_heloisa_duplicates())
