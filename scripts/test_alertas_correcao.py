import sys
import os
import asyncio
from datetime import datetime, timedelta, timezone

# Adiciona o diretório 'src' ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from resources.database import Base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from models.alerta import Alerta
from models.historico_acao import HistoricoAcao
from models.solicitacao_alta import SolicitacaoAlta
from models.solicitacao_leito import SolicitacaoLeito
from models.leito_estado import LeitoEstado

from providers.implementations.alerta_provider import AlertaProvider
from providers.implementations.solicitacao_alta_provider import SolicitacaoAltaProvider
from providers.implementations.solicitacao_leito_provider import SolicitacaoLeitoProvider
from providers.implementations.historico_provider import HistoricoProvider
from controllers.alerta_controller import AlertaController

class MockLeitosController:
    async def listar_leitos(self):
        return []

async def test_alertas_correcao():
    print("Iniciando testes de correção de alertas...")
    
    # 1. Configurar banco SQLite temporário em memória
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session() as session:
        # Instanciar provedores e controller
        alerta_provider = AlertaProvider(session=session)
        alta_provider = SolicitacaoAltaProvider(session=session)
        solicitacao_provider = SolicitacaoLeitoProvider(session=session)
        historico_provider = HistoricoProvider(session=session)
        mock_leitos_controller = MockLeitosController()
        
        controller = AlertaController(
            alerta_provider=alerta_provider,
            leitos_controller=mock_leitos_controller,
            alta_provider=alta_provider,
            solicitacao_leito_provider=solicitacao_provider,
            historico_provider=historico_provider
        )
        
        # Testar 1: Normalização de data
        print("\n--- Testando 1: Normalização de Datas ---")
        assert controller._normalizar_data("27-05-2026") == "2026-05-27"
        assert controller._normalizar_data("27/05/2026") == "2026-05-27"
        assert controller._normalizar_data("2026-05-27") == "2026-05-27"
        assert controller._normalizar_data("2026-05-27 10:30:00") == "2026-05-27"
        assert controller._normalizar_data("2026-05-27T10:30:00.123Z") == "2026-05-27"
        print("[OK] Normalização de datas validada com sucesso.")
        
        # Testar 2: Geração de alerta de cirurgia para hoje
        print("\n--- Testando 2: Geração de alerta para hoje ---")
        # Define datas
        hoje_dt = datetime.now() - timedelta(hours=3) # Horário de Brasília
        hoje_str = hoje_dt.strftime("%Y-%m-%d")
        hoje_dd_mm_yyyy = hoje_dt.strftime("%d-%m-%y") # DD-MM-YY ou DD-MM-YYYY
        hoje_full_format = hoje_dt.strftime("%d-%m-%Y")
        
        amanha_dt = hoje_dt + timedelta(days=1)
        amanha_full_format = amanha_dt.strftime("%d-%m-%Y")
        
        # Criar solicitacoes (vagas) no banco
        # Solicitação 1: Cirurgia para hoje (formato DD-MM-YYYY)
        sol_hoje = await solicitacao_provider.criar({
            "prontuario": "111",
            "nome": "PACIENTE HOJE",
            "idade": 30,
            "especialidade": "GERAL",
            "procedimento": "CIRURGIA HOJE",
            "tipo": "Cirurgico",
            "turno": "Manhã",
            "data_cirurgia": hoje_full_format,
            "hora_cirurgia": "08:00",
            "status": "Pendente",
            "perfil_solicitante": "BC"
        })
        
        # Solicitação 2: Cirurgia para amanhã (formato DD-MM-YYYY)
        sol_amanha = await solicitacao_provider.criar({
            "prontuario": "222",
            "nome": "PACIENTE AMANHA",
            "idade": 40,
            "especialidade": "GERAL",
            "procedimento": "CIRURGIA AMANHA",
            "tipo": "Cirurgico",
            "turno": "Tarde",
            "data_cirurgia": amanha_full_format,
            "hora_cirurgia": "14:00",
            "status": "Pendente",
            "perfil_solicitante": "BC"
        })
        
        # Criar eventos no histórico
        ev_hoje = await historico_provider.registrar(
            operador="BC",
            tipo="nova_solicitacao",
            acao="Nova solicitação criada",
            detalhes=f"Nova solicitação de leito criada para o prontuário 111. #{sol_hoje.id}",
            prontuario="111"
        )
        
        ev_amanha = await historico_provider.registrar(
            operador="BC",
            tipo="nova_solicitacao",
            acao="Nova solicitação criada",
            detalhes=f"Nova solicitação de leito criada para o prontuário 222. #{sol_amanha.id}",
            prontuario="222"
        )
        
        # Gerar alertas
        await controller.gerar_alertas()
        
        # Verificar alertas gerados
        alertas = await alerta_provider.get_todos()
        print(f"Alertas gerados: {[a.titulo for a in alertas]}")
        
        # Deve ter gerado o alerta do prontuário 111 (hoje), mas não do 222 (amanhã)
        prontuarios_alertados = [a.prontuario for a in alertas]
        assert "111" in prontuarios_alertados, "Prontuário 111 (hoje) deveria ter gerado um alerta"
        assert "222" not in prontuarios_alertados, "Prontuário 222 (amanhã) NÃO deveria ter gerado um alerta"
        print("[OK] Alertas filtrados por data 'para hoje' corretamente.")
        
        # Testar 3: Deduplicação de alertas
        print("\n--- Testando 3: Deduplicação de Alertas ---")
        # Executar gerar_alertas novamente
        await controller.gerar_alertas()
        
        # O número de alertas deve continuar sendo o mesmo (não deve duplicar)
        alertas_pos = await alerta_provider.get_todos()
        assert len(alertas_pos) == len(alertas), f"Deduplicação falhou. Esperava {len(alertas)} alertas, obteve {len(alertas_pos)}."
        print("[OK] Deduplicação funcionou perfeitamente para execuções consecutivas.")
        
        # Testar timezone e microsecond tolerance
        # Simula um novo evento na lista que tem uma pequena variação de segundos ou fuso
        alertas_manter_ids = []
        # Adiciona um alerta na base com timestamp ligeiramente diferente
        data_teste = {
            "tipo": "info",
            "categoria": "Gargalo",
            "titulo": "Nova solicitação para hoje",
            "mensagem": ev_hoje.detalhes,
            "prontuario": "111",
            "perfil_alvo": None,
            "criado_em": ev_hoje.criado_em + timedelta(seconds=1.5) # 1.5s de diferença
        }
        
        # Sincroniza
        res = await controller._sincronizar_alertas([data_teste])
        alertas_finais = await alerta_provider.get_todos()
        # Não deve ter inserido nenhum novo alerta (deve ter retornado o id existente)
        # Como o alerta original já estava na base, len(alertas_finais) deve continuar a mesma
        assert len(alertas_finais) == len(alertas), "Deduplicação falhou ao comparar timestamps com pequena diferença"
        print("[OK] Tolerância de timestamp na deduplicação validada com sucesso.")
        
        # Testar 4: Solicitações Canceladas no Histórico
        print("\n--- Testando 4: Solicitações Canceladas no Histórico ---")
        # Criar uma solicitação que é marcada como cancelada
        sol_cancelada = await solicitacao_provider.criar({
            "prontuario": "333",
            "nome": "PACIENTE CANCELADO",
            "idade": 50,
            "especialidade": "UTI",
            "procedimento": "PROCEDIMENTO",
            "tipo": "Cirurgico",
            "turno": "Manhã",
            "data_cirurgia": hoje_full_format,
            "hora_cirurgia": "10:00",
            "status": "Cancelada",
            "perfil_solicitante": "BC"
        })
        
        # Criar evento correspondente
        ev_cancelamento = await historico_provider.registrar(
            operador="UTI",
            tipo="cancelamento_reserva",
            acao="Reserva cancelada",
            detalhes=f"Reserva cancelada para o prontuário 333. #{sol_cancelada.id}",
            prontuario="333"
        )
        
        # Executar gerar_alertas
        await controller.gerar_alertas()
        
        # Deve ter processado o cancelamento e recuperado o perfil do solicitante (BC)
        alertas_finais = await alerta_provider.get_todos()
        alertas_cancelamento = [a for a in alertas_finais if a.prontuario == "333"]
        assert len(alertas_cancelamento) > 0, "Deveria ter gerado alerta para o cancelamento"
        # O perfil alvo deve ser "BC" (vindo de perfil_solicitante da vaga/solicitacao)
        assert alertas_cancelamento[0].perfil_alvo == "BC", f"Perfil alvo esperado 'BC', obteve '{alertas_cancelamento[0].perfil_alvo}'"
        print("[OK] Solicitações canceladas integradas com sucesso ao histórico de alertas.")

    print("\nTodos os testes passaram com sucesso!")

if __name__ == "__main__":
    asyncio.run(test_alertas_correcao())
