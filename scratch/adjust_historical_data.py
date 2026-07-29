import sys
import os
from sqlalchemy import select, update
from datetime import datetime

# Importar o gerenciador de banco de dados da aplicação
sys.path.insert(0, '/app/src')
from resources.database import DatabaseManager
from models.historico_acao import HistoricoAcao
from models.alerta import Alerta

async def adjust():
    dsn = os.getenv("SQLITE_DSN") or "sqlite+aiosqlite:////app/data/app.db"
    db = DatabaseManager(dsn)
    await db.initialize()
    
    async with db.get_session() as session:
        # 1. Atualizar o histórico de ações
        print("Buscando histórico de trocas de paciente antigas...")
        res_hist = await session.execute(
            select(HistoricoAcao).where(
                HistoricoAcao.tipo == "cancelamento_reserva"
            )
        )
        historicos = res_hist.scalars().all()
        
        hist_count = 0
        for h in historicos:
            det = (h.detalhes or "").lower()
            if "troca de paciente" in det or "substituído pelo" in det or "mesclado" in det:
                h.tipo = "cancelamento_solicitante"
                h.acao = "Cancelou reserva de leito (Troca de Paciente)"
                hist_count += 1
        
        # 2. Atualizar alertas antigos correspondentes
        print("Buscando alertas de cancelamento de reservas antigos...")
        res_alertas = await session.execute(
            select(Alerta).where(
                Alerta.titulo == "Reserva Cancelada pela UTI"
            )
        )
        alertas = res_alertas.scalars().all()
        
        alert_count = 0
        for a in alertas:
            msg = (a.mensagem or "").lower()
            if "troca de paciente" in msg or "substituído pelo" in msg or "mesclado" in msg:
                a.titulo = "Reserva Remanejada (Troca de Paciente)"
                a.tipo = "aviso"
                if not a.lido:
                    a.lido = True
                    a.lido_em = a.criado_em or datetime.utcnow()
                    a.lido_por = "Sistema"
                alert_count += 1
                
        await session.commit()
        print(f"Sucesso! {hist_count} registros de histórico e {alert_count} alertas antigos foram corrigidos.")
        
    await db.close_connection()

if __name__ == "__main__":
    import asyncio
    asyncio.run(adjust())
