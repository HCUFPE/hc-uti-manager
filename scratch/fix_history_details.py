import sys
import os
from sqlalchemy import select, delete, update

# Importar o gerenciador de banco de dados da aplicação
sys.path.insert(0, '/app/src')
from resources.database import DatabaseManager
from models.alerta import Alerta
from models.historico_acao import HistoricoAcao

async def fix_history():
    dsn = os.getenv("SQLITE_DSN") or "sqlite+aiosqlite:////app/data/app.db"
    db = DatabaseManager(dsn)
    
    async for session in db.get_session():
        # 1. Atualizar o texto do histórico antigo para incluir a tag de troca
        print("Atualizando detalhes do evento histórico 511...")
        await session.execute(
            update(HistoricoAcao)
            .where(HistoricoAcao.id == 511)
            .values(detalhes="Solicitação #96 (Prontuário 13938907) para Leito 0502G (Gerada via troca de paciente)")
        )
        
        # 2. Deletar o alerta de reserva correspondente a este prontuário (13938907)
        print("Deletando o alerta de reserva redundante...")
        await session.execute(
            delete(Alerta).where(
                Alerta.prontuario == "13938907",
                Alerta.titulo == "Vaga Reservada pela UTI"
            )
        )
        
        await session.commit()
        print("Correção de histórico e remoção do alerta executados com sucesso!")
        
    await db.close_connection()

if __name__ == "__main__":
    import asyncio
    asyncio.run(fix_history())
