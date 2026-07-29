import sys
import os
from sqlalchemy import select, delete

# Importar o gerenciador de banco de dados da aplicação
sys.path.insert(0, '/app/src')
from resources.database import DatabaseManager
from models.alerta import Alerta

async def merge_alerts():
    dsn = os.getenv("SQLITE_DSN") or "sqlite+aiosqlite:////app/data/app.db"
    db = DatabaseManager(dsn)
    
    async for session in db.get_session():
        # 1. Troca para 22307987: Deletar o alerta duplicado de vaga reservada (ID 311)
        print("Deletando alerta duplicado ID 311...")
        await session.execute(delete(Alerta).where(Alerta.id == 311))
        
        # 2. Troca para 13938907: Deletar alertas duplicados (IDs 317 e 318)
        print("Deletando alertas duplicados ID 317 e 318...")
        await session.execute(delete(Alerta).where(Alerta.id.in_([317, 318])))
        
        # 3. Atualizar o alerta ID 319 para ser o unificado
        print("Atualizando alerta ID 319 para ser o unificado de remanejamento...")
        res = await session.execute(select(Alerta).where(Alerta.id == 319))
        alerta_319 = res.scalar_one_or_none()
        if alerta_319:
            alerta_319.titulo = "Reserva Remanejada (Troca de Paciente)"
            alerta_319.tipo = "aviso"
            alerta_319.mensagem = "Solicitação #92 (Paciente A - 21036074) foi cancelada e o Leito 0502G foi transferido para o Paciente B (Paciente 13938907) via troca de paciente."
            alerta_319.lido = True
            alerta_319.lido_em = alerta_319.criado_em
            alerta_319.lido_por = "Sistema"
            
        await session.commit()
        print("Fusão e consolidação dos alertas concluídas com sucesso!")
        
    await db.close_connection()

if __name__ == "__main__":
    import asyncio
    asyncio.run(merge_alerts())
