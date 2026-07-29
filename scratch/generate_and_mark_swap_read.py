import sys
import os
from datetime import datetime

# Importar controllers da aplicação
sys.path.insert(0, '/app/src')
from resources.database import DatabaseManager
from controllers.alerta_controller import AlertaController
from models.alerta import Alerta

async def run_process():
    dsn = os.getenv("SQLITE_DSN") or "sqlite+aiosqlite:////app/data/app.db"
    db = DatabaseManager(dsn)
    
    # 1. Gerar novos alertas
    print("Executando o motor de geração de alertas...")
    controller = AlertaController(db)
    await controller.gerar_novos_alertas()
    
    # 2. Buscar e marcar como lido o alerta de remanejamento da troca do Damião
    async for session in db.get_session():
        from sqlalchemy import select
        res = await session.execute(
            select(Alerta).where(
                Alerta.prontuario == "22064729",
                Alerta.titulo == "Reserva Remanejada (Troca de Paciente)"
            )
        )
        alerta = res.scalar_one_or_none()
        if alerta:
            print(f"Alerta ID {alerta.id} encontrado. Marcando como lido pelo Sistema...")
            alerta.lido = True
            alerta.lido_por = "Sistema"
            alerta.lido_em = datetime.utcnow()
            await session.commit()
            print("Status do alerta atualizado com sucesso!")
        else:
            print("Alerta de remanejamento para 22064729 não encontrado (talvez já tenha sido processado ou ainda não gerado).")
            
    await db.close_connection()

if __name__ == "__main__":
    import asyncio
    asyncio.run(run_process())
