import sys
import os
from sqlalchemy import update, delete

# Importar o gerenciador de banco de dados da aplicação
sys.path.insert(0, '/app/src')
from resources.database import DatabaseManager
from models.alerta import Alerta
from models.historico_acao import HistoricoAcao

async def fix_new_swap():
    dsn = os.getenv("SQLITE_DSN") or "sqlite+aiosqlite:////app/data/app.db"
    db = DatabaseManager(dsn)
    
    async for session in db.get_session():
        # 1. Corrigir o log de histórico ID 534 (substituindo placeholders e Leito Leito)
        print("Corrigindo nomes e prefixo Leito no evento histórico 534...")
        await session.execute(
            update(HistoricoAcao)
            .where(HistoricoAcao.id == 534)
            .values(detalhes="Solicitação #100 (JOSE CARLOS DE LUCENA) foi reservada para o Leito 0502F. Motivo: Recebeu a vaga de DAMIAO ALVES PEREIRA (Prontuário 22064729) via troca de paciente.")
        )
        
        # 2. Adicionar tag (Gerada via troca de paciente) no evento histórico 535
        print("Adicionando tag de troca no evento histórico 535...")
        await session.execute(
            update(HistoricoAcao)
            .where(HistoricoAcao.id == 535)
            .values(detalhes="Solicitação #100 (Prontuário 21931076) para Leito 0502F (Gerada via troca de paciente)")
        )
        
        # 3. Deletar o alerta de reserva correspondente a este prontuário (21931076)
        print("Deletando o alerta de reserva redundante...")
        await session.execute(
            delete(Alerta).where(
                Alerta.prontuario == "21931076",
                Alerta.titulo == "Vaga Reservada pela UTI"
            )
        )
        
        await session.commit()
        print("Correção do histórico e remoção do alerta executados com sucesso!")
        
    await db.close_connection()

if __name__ == "__main__":
    import asyncio
    asyncio.run(fix_new_swap())
