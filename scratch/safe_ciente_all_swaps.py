import sys
import os
from sqlalchemy import select
from datetime import datetime

# Importar o gerenciador de banco de dados da aplicação
sys.path.insert(0, '/app/src')
from resources.database import DatabaseManager
from models.alerta import Alerta

async def safe_mark():
    dsn = os.getenv("SQLITE_DSN") or "sqlite+aiosqlite:////app/data/app.db"
    db = DatabaseManager(dsn)
    
    async for session in db.get_session():
        prontuarios_troca = ["21036074", "22307987", "13938907"]
        print(f"Buscando todos os alertas para prontuários: {prontuarios_troca}")
        
        res = await session.execute(
            select(Alerta).where(Alerta.prontuario.in_(prontuarios_troca))
        )
        alertas = res.scalars().all()
        
        for a in alertas:
            print(f"Processando Alerta ID {a.id} | Titulo: {a.titulo}...")
            
            # Forçar Lido como True e ciente via Sistema
            a.lido = True
            a.lido_por = "Sistema"
            if not a.lido_em:
                a.lido_em = datetime.utcnow()
                
            # Se for uma notificação de troca/substituição, padroniza o título
            msg_lower = a.mensagem.lower()
            if "substitu" in msg_lower or "troca de paciente" in msg_lower:
                print(f"  -> Padronizando título do Alerta ID {a.id} para Reserva Remanejada...")
                a.titulo = "Reserva Remanejada (Troca de Paciente)"
                a.tipo = "aviso"
                
        await session.commit()
        print("Marcação de cientes segura concluída!")
        
    await db.close_connection()

if __name__ == "__main__":
    import asyncio
    asyncio.run(safe_mark())
