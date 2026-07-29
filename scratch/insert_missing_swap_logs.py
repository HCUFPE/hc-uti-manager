import sys
import os
from datetime import datetime

# Importar o gerenciador de banco de dados da aplicação
sys.path.insert(0, '/app/src')
from resources.database import DatabaseManager
from models.historico_acao import HistoricoAcao

async def insert_logs():
    dsn = os.getenv("SQLITE_DSN") or "sqlite+aiosqlite:////app/data/app.db"
    db = DatabaseManager(dsn)
    
    async for session in db.get_session():
        # 1. Troca 2: Heloísa (21036074) -> 13938907 no Leito 0502G (ocorrida às ~07:59 local / 10:59 UTC)
        print("Inserindo log de cancelamento de reserva para a troca da Heloísa...")
        log_heloisa = HistoricoAcao(
            operador="Sistema",
            tipo="cancelamento_solicitante",
            acao="Cancelou reserva de leito (Troca de Paciente)",
            detalhes="Solicitação #92 (HELOISA SIQUEIRA FERNANDES) teve sua reserva no Leito 0502G cancelada. Motivo: Foi substituído por Prontuário 13938907 via troca de paciente.",
            prontuario="21036074",
            criado_em=datetime.fromisoformat("2026-07-29 10:59:05.951300")
        )
        session.add(log_heloisa)
        
        # 2. Troca 3: Damião (22064729) -> José Carlos (21931076) no Leito 0502F (ocorrida às ~14:27 local / 17:27 UTC)
        print("Inserindo log de cancelamento de reserva para a troca do Damião...")
        log_damiao = HistoricoAcao(
            operador="jackeline.vieira",
            tipo="cancelamento_solicitante",
            acao="Cancelou reserva de leito (Troca de Paciente)",
            detalhes="Solicitação #60 (DAMIAO ALVES PEREIRA) teve sua reserva no Leito 0502F cancelada. Motivo: Foi substituído por JOSE CARLOS DE LUCENA (Prontuário 21931076) via troca de paciente.",
            prontuario="22064729",
            criado_em=datetime.fromisoformat("2026-07-29 17:27:19.905922")
        )
        session.add(log_damiao)
        
        await session.commit()
        print("Registros inseridos e indicadores retroativos atualizados com sucesso!")
        
    await db.close_connection()

if __name__ == "__main__":
    import asyncio
    asyncio.run(insert_logs())
