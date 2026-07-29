import sys
import os
from sqlalchemy import select

# Importar o gerenciador de banco de dados da aplicação
sys.path.insert(0, '/app/src')
from resources.database import DatabaseManager
from models.alerta import Alerta

async def update_ciente():
    dsn = os.getenv("SQLITE_DSN") or "sqlite+aiosqlite:////app/data/app.db"
    db = DatabaseManager(dsn)
    
    async for session in db.get_session():
        print("Buscando alertas de remanejamento ativos para atualizar assinatura...")
        res = await session.execute(
            select(Alerta).where(
                Alerta.prontuario == "21036074",
                Alerta.titulo == "Reserva Remanejada (Troca de Paciente)"
            )
        )
        alertas = res.scalars().all()
        for a in alertas:
            a.lido_por = "Sistema"
            
        await session.commit()
        print(f"Sucesso! {len(alertas)} alertas atualizados com ciente via 'Sistema'.")
        
    await db.close_connection()

if __name__ == "__main__":
    import asyncio
    asyncio.run(update_ciente())
