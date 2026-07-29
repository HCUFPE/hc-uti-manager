import sys
import os
from datetime import datetime

# Importar o gerenciador de banco de dados da aplicação
sys.path.insert(0, '/app/src')
from resources.database import DatabaseManager
from models.alerta import Alerta
from models.historico_acao import HistoricoAcao

async def process_standardization():
    dsn = os.getenv("SQLITE_DSN") or "sqlite+aiosqlite:////app/data/app.db"
    db = DatabaseManager(dsn)
    
    async for session in db.get_session():
        from sqlalchemy import select, update
        
        # --- ALERTA 332 (Mariano -> Heloísa) ---
        print("Padronizando Alerta 332...")
        await session.execute(
            update(Alerta)
            .where(Alerta.id == 332)
            .values(mensagem="Solicitação #92 (MARIANO JUSTINO DANTAS - Prontuário 21036074) teve sua reserva no Leito 0502G cancelada. Motivo: Foi substituído por HELOISA SIQUEIRA FERNANDES (Prontuário 22307987) via troca de paciente.")
        )
        
        # --- LOG correspondente à Troca Mariano -> Heloísa no histórico ---
        print("Padronizando Log histórico correspondente...")
        await session.execute(
            update(HistoricoAcao)
            .where(
                HistoricoAcao.prontuario == "21036074",
                HistoricoAcao.tipo == "cancelamento_solicitante",
                HistoricoAcao.detalhes.like("%22307987%")
            )
            .values(detalhes="Solicitação #92 (MARIANO JUSTINO DANTAS - Prontuário 21036074) teve sua reserva no Leito 0502G cancelada. Motivo: Foi substituído por HELOISA SIQUEIRA FERNANDES (Prontuário 22307987) via troca de paciente.")
        )
        
        # --- ALERTA 342 (Heloísa -> Gisele) ---
        print("Padronizando Alerta 342...")
        await session.execute(
            update(Alerta)
            .where(Alerta.id == 342)
            .values(mensagem="Solicitação #92 (HELOISA SIQUEIRA FERNANDES - Prontuário 22307987) teve sua reserva no Leito 0502G cancelada. Motivo: Foi substituído por GISELE MARIA DA SILVA (Prontuário 13938907) via troca de paciente.")
        )
        
        # --- LOG correspondente à Troca Heloísa -> Gisele no histórico (e inversão de ordem) ---
        print("Padronizando e ajustando ordem do Log Heloísa -> Gisele...")
        await session.execute(
            update(HistoricoAcao)
            .where(
                HistoricoAcao.prontuario == "21036074",
                HistoricoAcao.tipo == "cancelamento_solicitante",
                HistoricoAcao.detalhes.like("%13938907%")
            )
            .values(
                detalhes="Solicitação #92 (HELOISA SIQUEIRA FERNANDES - Prontuário 22307987) teve sua reserva no Leito 0502G cancelada. Motivo: Foi substituído por GISELE MARIA DA SILVA (Prontuário 13938907) via troca de paciente.",
                criado_em=datetime.fromisoformat("2026-07-29 10:59:06.951300") # +1s em relação à exclusão
            )
        )
        
        # --- ALERTA 343 (Damião -> José Carlos) ---
        print("Padronizando Alerta 343...")
        await session.execute(
            update(Alerta)
            .where(Alerta.id == 343)
            .values(mensagem="Solicitação #60 (DAMIAO ALVES PEREIRA - Prontuário 22064729) teve sua reserva no Leito 0502F cancelada. Motivo: Foi substituído por JOSE CARLOS DE LUCENA (Prontuário 21931076) via troca de paciente.")
        )
        
        # --- LOG correspondente à Troca Damião -> José Carlos no histórico (e inversão de ordem) ---
        print("Padronizando e ajustando ordem do Log Damião -> José Carlos...")
        await session.execute(
            update(HistoricoAcao)
            .where(
                HistoricoAcao.prontuario == "22064729",
                HistoricoAcao.tipo == "cancelamento_solicitante",
                HistoricoAcao.detalhes.like("%21931076%")
            )
            .values(
                detalhes="Solicitação #60 (DAMIAO ALVES PEREIRA - Prontuário 22064729) teve sua reserva no Leito 0502F cancelada. Motivo: Foi substituído por JOSE CARLOS DE LUCENA (Prontuário 21931076) via troca de paciente.",
                criado_em=datetime.fromisoformat("2026-07-29 17:27:20.905922") # +1s em relação à exclusão
            )
        )
        
        await session.commit()
        print("Padronização e ordenação no banco concluídas com sucesso!")
        
    await db.close_connection()

if __name__ == "__main__":
    import asyncio
    asyncio.run(process_standardization())
