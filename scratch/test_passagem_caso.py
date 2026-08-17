import asyncio
import os
import sys
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import select

# Adiciona o diretório 'src' ao PATH para importar os módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from resources.database import Base
from models.leito_estado import LeitoEstado
from models.solicitacao_leito import SolicitacaoLeito
from models.historico_acao import HistoricoAcao
from providers.implementations.leito_estado_provider import LeitoEstadoProvider
from controllers.leitos_controller import LeitosController
from controllers.solicitacao_leito_controller import SolicitacaoLeitoController

class MockCensusProvider:
    def __init__(self, leitos=None):
        self.leitos = leitos or []
    async def listar_leitos(self):
        return self.leitos

class MockHistoricoProvider:
    def __init__(self, session):
        self.session = session
        self.logs = []
    async def registrar(self, operador, tipo, acao, detalhes, prontuario=None):
        log = HistoricoAcao(
            operador=operador,
            tipo=tipo,
            acao=acao,
            detalhes=detalhes,
            prontuario=prontuario
        )
        self.session.add(log)
        await self.session.commit()
        self.logs.append(log)

class MockLeitoEstadoProvider:
    def __init__(self, session):
        self.session = session

    async def get_por_id(self, sol_id):
        result = await self.session.execute(select(SolicitacaoLeito).where(SolicitacaoLeito.id == sol_id))
        return result.scalar_one_or_none()

    async def get_todas(self):
        result = await self.session.execute(select(SolicitacaoLeito))
        return result.scalars().all()

    async def atualizar(self, sol_id, values):
        sol = await self.get_por_id(sol_id)
        if sol:
            for k, v in values.items():
                setattr(sol, k, v)
            await self.session.commit()

    async def obter_todos_estados(self):
        result = await self.session.execute(select(LeitoEstado))
        return result.scalars().all()

async def test_passagem_caso():
    # 1. Setup Banco em Memória
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    async with async_session() as session:
        # Iniciar provedores e mock providers
        leito_estado_provider = LeitoEstadoProvider(session)
        sol_provider = MockLeitoEstadoProvider(session)
        historico_provider = MockHistoricoProvider(session)
        census_provider = MockCensusProvider()
        
        controller_sol = SolicitacaoLeitoController(
            leito_provider=sol_provider,
            aghu_cirurgia_provider=None
        )
        
        controller_leitos = LeitosController(
            estado_provider=leito_estado_provider,
            census_provider=census_provider,
            solicitacao_provider=sol_provider,
            historico_provider=historico_provider
        )
        
        # 2. Criar uma solicitação com leito reservado e cirurgia ativa
        print("Criando solicitação de teste...")
        sol = SolicitacaoLeito(
            prontuario="99999",
            nome="PACIENTE TESTE PASSAGEM",
            idade=45,
            especialidade="Cardiologia",
            tipo="Cirúrgico",
            status="Reservado",
            turno="Tarde",
            destino="Leito 01",
            prioridade="P1",
            perfil_solicitante="BC"
        )
        session.add(sol)
        await session.commit()
        await session.refresh(sol)
        
        # Vincular no leito_estados
        est = LeitoEstado(
            lto_id="LEITO 01",
            alta_solicitada=False,
            prontuario_proximo=99999,
            idade_proximo=45,
            especialidade_proximo="Cardiologia",
            solicitacao_id=sol.id
        )
        session.add(est)
        await session.commit()
        
        print(f"Solicitação criada com ID #{sol.id} e Leito 01 reservado.")
        
        # 3. Finalizar cirurgia com Passagem de Caso
        print("Finalizando cirurgia com dados de Passagem de Caso...")
        texto_clinico = "Paciente cardiopata, instabilidade hemodinâmica, uso de Noradrenalina 0.2mcg/kg/min."
        await controller_sol.marcar_cirurgia_finalizada(sol.id, passagem_caso=texto_clinico)
        
        # Verificar no banco
        sol_atualizado = await sol_provider.get_por_id(sol.id)
        assert sol_atualizado.cirurgia_finalizada is True, "Cirurgia deveria estar finalizada"
        assert sol_atualizado.passagem_caso == texto_clinico, "Passagem de caso deveria estar gravada no banco"
        print("Finalização com passagem de caso gravada com sucesso no SQLite!")
        
        # 4. Verificar exposição na listagem de leitos
        print("Verificando exposição da Passagem de Caso no censo de leitos...")
        census_provider.leitos = [
            {"lto_lto_id": "Leito 01", "status": "Desocupado", "tipo": "uti", "prontuario_atual": None}
        ]
        
        leitos_result = await controller_leitos.listar_leitos()
        leito_01 = next((l for l in leitos_result if l["lto_lto_id"] == "LEITO 01"), None)
        
        assert leito_01 is not None, "Leito 01 deveria estar presente no resultado"
        assert leito_01.get("passagem_caso") == texto_clinico, "Exposição direta de passagem_caso falhou no leito"
        print("Passagem de caso exposta corretamente no objeto do Leito para o frontend!")
        
        print("\n=== TODOS OS TESTES PASSARAM COM SUCESSO! ===")

if __name__ == "__main__":
    asyncio.run(test_passagem_caso())
