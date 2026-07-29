import sys
import os
from datetime import datetime

# Importar controllers e providers da aplicação
sys.path.insert(0, '/app/src')
from resources.database import DatabaseManager
from models.alerta import Alerta

from providers.implementations.alerta_provider import AlertaProvider
from providers.implementations.leito_estado_provider import LeitoEstadoProvider
from providers.implementations.solicitacao_alta_provider import SolicitacaoAltaProvider
from providers.implementations.solicitacao_leito_provider import SolicitacaoLeitoProvider
from providers.implementations.historico_provider import HistoricoProvider
from controllers.leitos_controller import LeitosController
from controllers.alerta_controller import AlertaController

async def run_process():
    dsn = os.getenv("SQLITE_DSN") or "sqlite+aiosqlite:////app/data/app.db"
    db = DatabaseManager(dsn)
    
    async for session in db.get_session():
        # Instanciar provedores com a sessão ativa
        alerta_prov = AlertaProvider(session)
        estado_prov = LeitoEstadoProvider(session)
        alta_prov = SolicitacaoAltaProvider(session)
        solicitacao_prov = SolicitacaoLeitoProvider(session)
        historico_prov = HistoricoProvider(session)
        
        # Constrói o LeitosController (sem censo do AGHU pois a rotina de alertas é local)
        leitos_ctrl = LeitosController(
            census_provider=None,
            estado_provider=estado_prov,
            alta_provider=alta_prov,
            solicitacao_provider=solicitacao_prov,
            historico_provider=historico_prov
        )
        
        # Constrói o AlertaController com todas as dependências injetadas
        controller = AlertaController(
            alerta_provider=alerta_prov,
            leitos_controller=leitos_ctrl,
            alta_provider=alta_prov,
            solicitacao_leito_provider=solicitacao_prov,
            historico_provider=historico_prov
        )
        
        # 1. Executar a rotina de novos alertas
        print("Executando o motor de geração de alertas...")
        await controller.gerar_novos_alertas()
        
        # 2. Buscar o alerta gerado para a troca do Damião e marcar como lido
        from sqlalchemy import select
        res = await session.execute(
            select(Alerta).where(
                Alerta.prontuario == "22064729",
                Alerta.titulo == "Reserva Remanejada (Troca de Paciente)"
            )
        )
        alerta = res.scalar_one_or_none()
        if alerta:
            print(f"Alerta ID {alerta.id} encontrado! Marcando como lido pelo Sistema...")
            alerta.lido = True
            alerta.lido_por = "Sistema"
            alerta.lido_em = datetime.utcnow()
            await session.commit()
            print("Status do alerta atualizado com sucesso!")
        else:
            print("Alerta de remanejamento para 22064729 não encontrado.")
            
    await db.close_connection()

if __name__ == "__main__":
    import asyncio
    asyncio.run(run_process())
