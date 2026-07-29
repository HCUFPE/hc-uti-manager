import sys
import os
from sqlalchemy import select, delete
from datetime import datetime

# Importar o gerenciador de banco de dados da aplicação
sys.path.insert(0, '/app/src')
from resources.database import DatabaseManager
from models.alerta import Alerta

async def run_fix():
    dsn = os.getenv("SQLITE_DSN") or "sqlite+aiosqlite:////app/data/app.db"
    db = DatabaseManager(dsn)
    
    async for session in db.get_session():
        # 1. Atualizar o alerta real gerado pelo motor (ID 334) para Lido/Sistema
        print("Buscando alerta real ID 334...")
        res = await session.execute(
            select(Alerta).where(
                Alerta.titulo == "Reserva Remanejada (Troca de Paciente)",
                Alerta.mensagem.like("%voltou para Pendente devido à troca de paciente%")
            )
        )
        alertas_reais = res.scalars().all()
        for a in alertas_reais:
            print(f"Atualizando ciente do alerta ID {a.id} para Sistema...")
            a.lido = True
            a.lido_em = datetime.utcnow()
            a.lido_por = "Sistema"
            
        # 2. Remover o alerta redundante genérico que inserimos no cleanup anterior (que tem "Paciente A")
        print("Removendo alerta genérico redundante...")
        await session.execute(
            delete(Alerta).where(
                Alerta.titulo == "Reserva Remanejada (Troca de Paciente)",
                Alerta.mensagem.like("%Paciente B (Prontuário 22307987)%")
            )
        )
        
        await session.commit()
        print("Ajuste de ciente concluído com sucesso!")
        
    await db.close_connection()

if __name__ == "__main__":
    import asyncio
    asyncio.run(run_fix())
