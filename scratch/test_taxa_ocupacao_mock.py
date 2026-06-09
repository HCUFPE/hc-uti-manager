import asyncio
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from providers.implementations.indicadores_provider import IndicadoresProvider

class MockCensusProvider:
    async def listar_leitos(self):
        # Retorna lista vazia para garantir que o provider utilize os mocks caso MOCK_BEDS=true
        return []

async def test_taxa_ocupacao_mock():
    os.environ["MOCK_BEDS"] = "true"
    
    database_url = "sqlite+aiosqlite:///c:/Users/daniel.turmina/Documents/HC-UTI-Manager/data/app.db"
    engine = create_async_engine(database_url, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        census_provider = MockCensusProvider()
        provider = IndicadoresProvider(session=session, census_provider=census_provider)

        print("Chamando get_indicadores_gerais com MOCK_BEDS=true...")
        indicadores = await provider.get_indicadores_gerais()
        
        ocupacao_resumo = indicadores.get("resumo", {}).get("ocupacao_atual", {})
        valor_ocupacao = ocupacao_resumo.get("valor")
        tendencia = ocupacao_resumo.get("tendencia")
        
        print(f"Taxa de ocupação calculada: {valor_ocupacao}")
        print(f"Tendência de ocupação: {tendencia}")
        
        assert valor_ocupacao == "50.0%", f"Esperava 50.0%, mas obteve {valor_ocupacao}"
        assert tendencia == "2 de 4 leitos", f"Esperava '2 de 4 leitos', mas obteve {tendencia}"
        
        print("Validação concluída com SUCESSO! A taxa de ocupação refletiu os leitos mockados corretamente.")

if __name__ == '__main__':
    asyncio.run(test_taxa_ocupacao_mock())
