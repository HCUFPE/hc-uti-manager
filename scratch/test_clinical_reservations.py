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

class MockSolicitacaoProvider:
    def __init__(self, session):
        self.session = session
    async def get_por_id(self, sol_id):
        result = await self.session.execute(select(SolicitacaoLeito).where(SolicitacaoLeito.id == sol_id))
        return result.scalar_one_or_none()
    async def concluir_admissao_se_pendente(self, sol_id):
        sol = await self.get_por_id(sol_id)
        if sol and sol.status != "Concluída":
            sol.status = "Concluída"
            await self.session.commit()
            return True
        return False
    async def atualizar(self, sol_id, values):
        sol = await self.get_por_id(sol_id)
        if sol:
            for k, v in values.items():
                setattr(sol, k, v)
            await self.session.commit()

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

async def test_all():
    # 1. Setup Banco em Memória
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    async with async_session() as session:
        # Instanciar Provedores
        estado_provider = LeitoEstadoProvider(session)
        sol_provider = MockSolicitacaoProvider(session)
        historico_provider = MockHistoricoProvider(session)
        census_provider = MockCensusProvider()
        
        # 2. Testar Tarefa 1.1: Column addition and provider save
        print("Executando Teste 1: Bloqueio e Cancelamento Clínico...")
        await estado_provider.salvar_bloqueio_clinico("UTI-01", True)
        
        # Buscar estado
        result = await session.execute(select(LeitoEstado).where(LeitoEstado.lto_id == "UTI-01"))
        est = result.scalar_one()
        assert est.bloqueado_clinico is True, "Bloqueio deveria ser True"
        
        # Cancelar bloqueio
        await estado_provider.salvar_bloqueio_clinico("UTI-01", False)
        assert est.bloqueado_clinico is False, "Bloqueio deveria ser False"
        print("Teste 1 com sucesso!")
        
        # 3. Testar Tarefa 2.2 e 2.3: listar_leitos mapping & Censo Auto-clean
        print("Executando Teste 2: Listagem de Leitos e Auto-limpeza pelo Censo...")
        census_provider.leitos = [
            {"lto_lto_id": "UTI-01", "status": "Desocupado", "tipo": "uti", "prontuario_atual": None},
            {"lto_lto_id": "UTI-02", "status": "Ocupado", "tipo": "uti", "prontuario_atual": "12345"}, # UTI-02 Ocupado fisicamente
        ]
        
        # UTI-01: Bloqueio ativo
        await estado_provider.salvar_bloqueio_clinico("UTI-01", True)
        # UTI-02: Bloqueio ativo (mas leito está fisicamente ocupado no censo)
        await estado_provider.salvar_bloqueio_clinico("UTI-02", True)
        
        controller = LeitosController(
            census_provider=census_provider,
            estado_provider=estado_provider,
            historico_provider=historico_provider
        )
        
        leitos = await controller.listar_leitos()
        
        # Verificar se UTI-01 retornou flag True
        uti01 = next(l for l in leitos if l["lto_lto_id"] == "UTI-01")
        assert uti01["bloqueado_clinico"] is True, "UTI-01 deveria estar com flag True"
        
        # Verificar se UTI-02 foi autolimpado pelo censo porque está ocupado fisicamente
        uti02 = next(l for l in leitos if l["lto_lto_id"] == "UTI-02")
        assert uti02["bloqueado_clinico"] is False, "UTI-02 deveria ter sido autolimpado"
        
        # Verificar se gravou histórico de autolimpeza
        assert len(historico_provider.logs) == 1, "Deveria ter registrado log de autolimpeza"
        assert "Auto-limpeza via censo" in historico_provider.logs[0].acao
        print("Teste 2 com sucesso!")
        
        # 4. Testar Tarefa 2.4: Filtragem de leitos disponíveis
        print("Executando Teste 3: Ocultação de leitos disponíveis bloqueados...")
        disponiveis = await controller.listar_leitos_disponiveis_para_reserva(incluir_reservados=False)
        # Como UTI-01 está com bloqueio clínico ativo, ele NÃO deve estar na lista de disponíveis
        nomes_disp = [d["lto_lto_id"] for d in disponiveis]
        assert "UTI-01" not in nomes_disp, "Leito UTI-01 bloqueado não deveria aparecer nos disponíveis"
        print("Teste 3 com sucesso!")
        
        # 5. Testar Tarefa 2.5: Swap Clínico no remanejamento
        print("Executando Teste 4: Swap Clínico no Remanejamento...")
        # Criar uma solicitação pendente reservada no leito UTI-03
        sol = SolicitacaoLeito(
            id=100,
            nome="PACIENTE ORIGEM",
            prontuario=999,
            idade=50,
            especialidade="CARDIOLOGIA",
            procedimento="CIRURGIA TESTE",
            tipo="cirurgico",
            turno="Manha",
            prioridade="Media",
            perfil_solicitante="NIR",
            status="Reservado",
            destino="Leito UTI-03",
            criado_em=datetime.now()
        )
        session.add(sol)
        
        # Reserva no local no UTI-03
        await estado_provider.salvar_reserva("UTI-03", prontuario=999, idade=50, especialidade="Clinica", solicitacao_id=100)
        
        # Bloquear UTI-04 para Clinico
        await estado_provider.salvar_bloqueio_clinico("UTI-04", True)
        
        sol_controller = SolicitacaoLeitoController(
            leito_provider=sol_provider,
            estado_provider=estado_provider,
            historico_provider=historico_provider
        )
        
        # Remanejar de UTI-03 para UTI-04 (que está com bloqueio clínico)
        result = await sol_controller.remanejar_reserva(sol_id=100, novo_leito_id="UTI-04")
        
        assert result.get("swap_clinico_ocorreu") is True, "Swap clínico deveria ter ocorrido"
        
        # Validar novos estados
        res_dest = await session.execute(select(LeitoEstado).where(LeitoEstado.lto_id == "UTI-04"))
        est_dest = res_dest.scalar_one()
        assert est_dest.prontuario_proximo == 999, "UTI-04 deveria conter o paciente 999"
        assert est_dest.bloqueado_clinico is False, "UTI-04 não deveria mais estar bloqueado clínico"
        
        res_orig = await session.execute(select(LeitoEstado).where(LeitoEstado.lto_id == "UTI-03"))
        est_orig = res_orig.scalar_one()
        assert est_orig.prontuario_proximo is None, "UTI-03 não deveria conter o paciente"
        assert est_orig.bloqueado_clinico is True, "UTI-03 deveria ter herdado o bloqueio clínico"
        
        print("Teste 4 com sucesso!")
        
    print("\n[OK] TODOS OS TESTES PASSARAM COM SUCESSO!")

if __name__ == "__main__":
    asyncio.run(test_all())
