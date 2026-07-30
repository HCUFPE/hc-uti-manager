import sys
import os
from datetime import datetime

# Importar o gerenciador de banco de dados da aplicação
sys.path.insert(0, '/app/src')
from resources.database import DatabaseManager
from models.alerta import Alerta
from models.historico_acao import HistoricoAcao

async def final_clean():
    dsn = os.getenv("SQLITE_DSN") or "sqlite+aiosqlite:////app/data/app.db"
    db = DatabaseManager(dsn)
    
    async for session in db.get_session():
        from sqlalchemy import delete, update
        
        # 1. Deletar todos os alertas antigos duplicados da Heloísa e do Damião
        print("Deletando alertas antigos de troca dos prontuários 21036074, 22307987, 22064729, 21931076...")
        await session.execute(
            delete(Alerta).where(
                Alerta.titulo == "Reserva Remanejada (Troca de Paciente)",
                Alerta.prontuario.in_(["21036074", "22307987", "22064729", "21931076", "13938907"])
            )
        )
        
        # 2. Reinserir um único alerta padrão correto e lido (Ciente) para cada uma das trocas
        print("Reinserindo alerta padronizado e assinado para a troca da Heloísa -> Gisele...")
        alerta_heloisa = Alerta(
            tipo="aviso",
            categoria="Gargalo",
            titulo="Reserva Remanejada (Troca de Paciente)",
            mensagem="Solicitação #92 (HELOISA SIQUEIRA FERNANDES - Prontuário 22307987) foi cancelada. Motivo: Foi substituído por GISELE MARIA DA SILVA (Prontuário 13938907) via troca de paciente.",
            prontuario="13938907",
            perfil_alvo=None,
            lido=True,
            lido_por="daniel.turmina",
            lido_em=datetime.fromisoformat("2026-07-29 16:58:00")
        )
        session.add(alerta_heloisa)
        
        print("Reinserindo alerta padronizado e assinado para a troca do Damião -> José Carlos...")
        alerta_damiao = Alerta(
            tipo="aviso",
            categoria="Gargalo",
            titulo="Reserva Remanejada (Troca de Paciente)",
            mensagem="Solicitação #60 (DAMIAO ALVES PEREIRA - Prontuário 22064729) foi cancelada. Motivo: Foi substituído por JOSE CARLOS DE LUCENA (Prontuário 21931076) via troca de paciente.",
            prontuario="21931076",
            perfil_alvo=None,
            lido=True,
            lido_por="daniel.turmina",
            lido_em=datetime.fromisoformat("2026-07-29 16:58:00")
        )
        session.add(alerta_damiao)
        
        # 3. Corrigir o prontuário, a data e a mensagem do histórico da Heloísa (22307987)
        # O log de cancelamento de reserva dela deve ir para o prontuário 22307987 e ficar 1s antes do de exclusão (10:59:04)
        print("Corrigindo prontuário e timestamp do log de cancelamento de reserva da Heloísa...")
        await session.execute(
            update(HistoricoAcao)
            .where(
                HistoricoAcao.tipo == "cancelamento_solicitante",
                HistoricoAcao.detalhes.like("%13938907%")
            )
            .values(
                prontuario="22307987",
                detalhes="Solicitação #92 (HELOISA SIQUEIRA FERNANDES - Prontuário 22307987) foi cancelada. Motivo: Foi substituído por GISELE MARIA DA SILVA (Prontuário 13938907) via troca de paciente.",
                criado_em=datetime.fromisoformat("2026-07-29 10:59:04.951300")
            )
        )
        
        # 4. Corrigir o timestamp e a mensagem do histórico do Damião (22064729)
        # O log de cancelamento de reserva dele deve ficar 1s antes do de exclusão (17:27:18)
        print("Corrigindo timestamp e mensagem do log de cancelamento de reserva do Damião...")
        await session.execute(
            update(HistoricoAcao)
            .where(
                HistoricoAcao.prontuario == "22064729",
                HistoricoAcao.tipo == "cancelamento_solicitante"
            )
            .values(
                detalhes="Solicitação #60 (DAMIAO ALVES PEREIRA - Prontuário 22064729) foi cancelada. Motivo: Foi substituído por JOSE CARLOS DE LUCENA (Prontuário 21931076) via troca de paciente.",
                criado_em=datetime.fromisoformat("2026-07-29 17:27:18.905922")
            )
        )
        
        await session.commit()
        print("Todos os ajustes finos foram aplicados com sucesso!")
        
    await db.close_connection()

if __name__ == "__main__":
    import asyncio
    asyncio.run(final_clean())
