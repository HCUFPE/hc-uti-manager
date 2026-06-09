import asyncio
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from models.solicitacao_leito import SolicitacaoLeito
from models.solicitacao_alta import SolicitacaoAlta
from models.historico_acao import HistoricoAcao
from providers.implementations.indicadores_provider import IndicadoresProvider

class MockCensusProvider:
    async def listar_leitos(self):
        return []

async def test_indicadores_sem_mock():
    # Garantir que ENV=development está ativo para testar a remoção do mock especificamente nesse ambiente
    os.environ["ENV"] = "development"
    
    database_url = "sqlite+aiosqlite:///c:/Users/daniel.turmina/Documents/HC-UTI-Manager/data/app.db"
    engine = create_async_engine(database_url, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        # Limpar tabelas locais
        await session.execute(SolicitacaoLeito.__table__.delete())
        await session.execute(SolicitacaoAlta.__table__.delete())
        await session.execute(HistoricoAcao.__table__.delete())
        await session.commit()

        census_provider = MockCensusProvider()
        provider = IndicadoresProvider(session=session, census_provider=census_provider)

        print("Chamando get_indicadores_gerais com banco de dados vazio...")
        indicadores = await provider.get_indicadores_gerais()
        
        tempo_medio = indicadores.get("detalhado", {}).get("tempo_liberacao_encaminhamento_minutos")
        print(f"Tempo médio obtido: {tempo_medio}")
        
        assert tempo_medio == 0.0, f"Esperava 0.0, mas obteve {tempo_medio}"
        print("Validação concluída: tempo médio de liberação de encaminhamento é 0.0 no banco de dados vazio!")
        print("SUCESSO: O mock de fallback do ambiente de desenvolvimento foi removido corretamete.")

if __name__ == '__main__':
    asyncio.run(test_indicadores_sem_mock())
