import sys
import os
import asyncio
from datetime import datetime, timedelta

# Adiciona o diretório 'src' ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from resources.database import Base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from models.solicitacao_leito import SolicitacaoLeito
from models.solicitacao_alta import SolicitacaoAlta
from models.historico_acao import HistoricoAcao
from providers.implementations.indicadores_provider import IndicadoresProvider

class MockCensusProvider:
    async def listar_leitos(self):
        return [
            {"lto_lto_id": "UTI-01", "status": "OCUPADO", "especialidade_atual": "CARDIOLOGIA", "prontuario_atual": "111111", "tempo_ocupacao": 2.5},
            {"lto_lto_id": "UTI-02", "status": "OCUPADO", "especialidade_atual": "NEUROLOGIA", "prontuario_atual": "222222", "tempo_ocupacao": 4.0},
            {"lto_lto_id": "UTI-03", "status": "DESOCUPADO", "prontuario_atual": None}
        ]

async def test_indicadores_fluxo():
    print("Iniciando testes de cálculo de indicadores de fluxo...")
    
    # 1. Configurar banco SQLite temporário em memória
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session() as session:
        # Instanciar provider
        census_provider = MockCensusProvider()
        provider = IndicadoresProvider(session=session, census_provider=census_provider)
        
        # 2. Criar Solicitações de Vaga
        print("\n--- Inserindo Solicitações de Vaga no Banco ---")
        
        # Solicitação 1: Bloco Cirúrgico (BC), Especialidade Cardiologia, Concluída
        sol1 = SolicitacaoLeito(
            prontuario="111111",
            nome="PACIENTE CARDIOLOGICO BC",
            idade=65,
            especialidade="CARDIOLOGIA",
            procedimento="REVASCULARIZACAO",
            tipo="Cirurgico",
            turno="Manha",
            status="Concluída",
            perfil_solicitante="BC",
            criado_em=datetime(2026, 5, 20, 6, 0, 0) # 06:00
        )
        session.add(sol1)
        
        # Solicitação 2: Hemodinâmica (HEM), Especialidade Cardiologia, Reservada (não concluída ainda)
        sol2 = SolicitacaoLeito(
            prontuario="222222",
            nome="PACIENTE HEMODINAMICA",
            idade=50,
            especialidade="CARDIOLOGIA",
            procedimento="CATETERISMO",
            tipo="HEM",
            turno="Tarde",
            status="Reservado",
            perfil_solicitante="HEM",
            criado_em=datetime(2026, 5, 21, 10, 0, 0)
        )
        session.add(sol2)
        
        # Solicitação 3: Comum/Clínico (CLI), Pendente
        sol3 = SolicitacaoLeito(
            prontuario="333333",
            nome="PACIENTE CLINICO",
            idade=70,
            especialidade="GERAL",
            procedimento=None,
            tipo="UTI",
            turno="Noite",
            status="Pendente",
            perfil_solicitante="UTI",
            criado_em=datetime(2026, 5, 22, 14, 0, 0)
        )
        session.add(sol3)

        # Solicitação 4: Cancelada
        sol4 = SolicitacaoLeito(
            prontuario="444444",
            nome="PACIENTE CANCELADO",
            idade=40,
            especialidade="GERAL",
            procedimento=None,
            tipo="Cirurgico",
            turno="Manha",
            status="Cancelada",
            perfil_solicitante="BC",
            criado_em=datetime(2026, 5, 20, 8, 0, 0)
        )
        session.add(sol4)
        
        await session.commit()
        
        # 3. Criar Solicitações de Alta
        print("--- Inserindo Solicitações de Alta no Banco ---")
        alta1 = SolicitacaoAlta(
            lto_id="UTI-01",
            prontuario="111111",
            leito_destino="Enfermaria 402",
            status="concluida",
            criado_em=datetime(2026, 5, 23, 12, 0, 0) # Alta solicitada 12:00
        )
        session.add(alta1)
        await session.commit()
        
        # 4. Inserir Eventos no Histórico de Ações
        print("--- Inserindo Eventos no Histórico de Ações ---")
        
        # Histórico da Solicitação 1
        h1 = HistoricoAcao(
            operador="sistema",
            tipo="solicitacao",
            acao="Criou solicitação",
            detalhes=f"Solicitação #{sol1.id}",
            prontuario="111111",
            criado_em=datetime(2026, 5, 20, 6, 0, 0)
        )
        # Reserva da Sol 1 às 08:00 (Turno Manha)
        h2 = HistoricoAcao(
            operador="dra_uti",
            tipo="reserva",
            acao="Reservou leito",
            detalhes=f"Leito UTI-01 reservado. Solicitação #{sol1.id}",
            prontuario="111111",
            criado_em=datetime(2026, 5, 20, 8, 0, 0)
        )
        # Fim cirúrgico da Sol 1 às 09:00
        h3 = HistoricoAcao(
            operador="enf_bc",
            tipo="cirurgia_finalizada",
            acao="Finalizou cirurgia",
            detalhes=f"Pronto para envio. Solicitação #{sol1.id}",
            prontuario="111111",
            criado_em=datetime(2026, 5, 20, 9, 0, 0)
        )
        # Admissão física da Sol 1 às 10:00 (Tempo recepção = 1h (60 min) | Tempo espera = 4h)
        h4 = HistoricoAcao(
            operador="Sistema (Censo)",
            tipo="conclusao",
            acao="Admissão concluída no leito UTI-01",
            detalhes=f"Paciente ocupou o leito UTI-01. Solicitação #{sol1.id} concluída automaticamente via censo.",
            prontuario="111111",
            criado_em=datetime(2026, 5, 20, 10, 0, 0)
        )
        
        # Histórico da Alta 1
        h5 = HistoricoAcao(
            operador="dra_uti",
            tipo="solicitacao_alta",
            acao="Solicitou alta",
            detalhes=f"Alta #{alta1.id}",
            prontuario="111111",
            criado_em=datetime(2026, 5, 23, 12, 0, 0)
        )
        # Destino NIR às 14:00 (Tempo acomodação = 2h)
        h6 = HistoricoAcao(
            operador="nir_user",
            tipo="alteracao_destino",
            acao="Definiu destino de alta",
            detalhes=f"Alta #{alta1.id}. Destino: Enfermaria 402",
            prontuario="111111",
            criado_em=datetime(2026, 5, 23, 14, 0, 0)
        )
        # Saída física da UTI às 15:00 (Tempo liberação = 1h | Tempo ocupação = 77h)
        h7 = HistoricoAcao(
            operador="Sistema (Censo)",
            tipo="conclusao_alta",
            acao="Alta concluída no leito UTI-01",
            detalhes=f"Paciente desocupou o leito UTI-01. Alta #{alta1.id} concluída automaticamente via censo.",
            prontuario="111111",
            criado_em=datetime(2026, 5, 23, 15, 0, 0)
        )

        # Histórico da Solicitação 2
        h8 = HistoricoAcao(
            operador="sistema",
            tipo="solicitacao",
            acao="Criou solicitação",
            detalhes=f"Solicitação #{sol2.id}",
            prontuario="222222",
            criado_em=datetime(2026, 5, 21, 10, 0, 0)
        )
        # Reserva da Sol 2 às 16:30 (Turno Tarde)
        h9 = HistoricoAcao(
            operador="dra_uti",
            tipo="reserva",
            acao="Reservou leito",
            detalhes=f"Leito UTI-02 reservado. Solicitação #{sol2.id}",
            prontuario="222222",
            criado_em=datetime(2026, 5, 21, 16, 30, 0)
        )

        # Histórico da Solicitação 4 (Cancelamento)
        h10 = HistoricoAcao(
            operador="enf_bc",
            tipo="cancelamento",
            acao="Exclusão de Solicitação",
            detalhes=f"Solicitação #{sol4.id} cancelada.",
            prontuario="444444",
            criado_em=datetime(2026, 5, 20, 8, 30, 0)
        )
        
        session.add_all([h1, h2, h3, h4, h5, h6, h7, h8, h9, h10])
        await session.commit()
        
        # 5. Executar cálculo de Indicadores com Filtro de Data
        # Filtro: 2026-05-19 a 2026-05-25 (Cobre todas as ações criadas)
        print("\n--- Calculando Indicadores Gerais com Filtro ---")
        dados = await provider.get_indicadores_gerais(data_inicio="2026-05-19", data_fim="2026-05-25")
        
        resumo = dados["resumo"]
        detalhado = dados["detalhado"]
        volumes = detalhado["volumes"]
        
        print("\n=== RESULTADOS DOS TESTES DE ASSERTIVIDADE ===")
        
        # 1. Taxa de ocupação (censo mockado: 2 ocupados de 3 leitos = 66.7%)
        print(f"Taxa de Ocupação Atual: {resumo['ocupacao_atual']['valor']} (Esperado: 66.7%)")
        assert "66.7%" in resumo["ocupacao_atual"]["valor"]
        
        # 2. Volumes do período (4 solicitações, 2 reservas, 1 concluída, 1 cancelamento solicitação, 1 alta)
        print(f"Volume Solicitações: {volumes['solicitacoes']} (Esperado: 4)")
        assert volumes["solicitacoes"] == 4
        print(f"Volume Concluídas: {volumes['concluidas']} (Esperado: 1)")
        assert volumes["concluidas"] == 1
        print(f"Volume Cancelamento Solicitações: {volumes['cancelamento_solicitacoes']} (Esperado: 1)")
        assert volumes["cancelamento_solicitacoes"] == 1
        
        # 3. Taxas de Atendimento e Cancelamento (1/4 = 25% cada)
        print(f"Taxa de Atendimento: {detalhado['taxas']['atendimento']}% (Esperado: 25.0%)")
        assert detalhado["taxas"]["atendimento"] == 25.0
        print(f"Taxa de Cancelamento: {detalhado['taxas']['cancelamento']}% (Esperado: 25.0%)")
        assert detalhado["taxas"]["cancelamento"] == 25.0

        # 4. Tempo médio de ocupação (77 horas para o único concluído)
        print(f"Tempo de Ocupação Médio Geral: {detalhado['tempo_ocupacao']['geral_horas']}h (Esperado: 77.0h)")
        assert detalhado["tempo_ocupacao"]["geral_horas"] == 77.0
        print(f"Tempo de Ocupação BC: {detalhado['tempo_ocupacao']['demandantes_horas']['BC']}h (Esperado: 77.0h)")
        assert detalhado["tempo_ocupacao"]["demandantes_horas"]["BC"] == 77.0
        
        # 5. Tempo médio de solicitação até ocupação (criado 06:00, ocupou 10:00 = 4.0h)
        print(f"Tempo de Solicitação até Ocupação: {detalhado['tempo_solicitacao_ocupacao_horas']}h (Esperado: 4.0h)")
        assert detalhado["tempo_solicitacao_ocupacao_horas"] == 4.0
        
        # 6. Horário médio de reserva
        # Turno Manhã: h2 criado_em = 08:00 UTC -> 05:00 Local
        # Turno Tarde: h9 criado_em = 16:30 UTC -> 13:30 Local
        print(f"Horário de Reserva Manhã: {detalhado['horario_reserva_turno']['manha']} (Esperado: 05:00)")
        assert detalhado["horario_reserva_turno"]["manha"] == "05:00"
        print(f"Horário de Reserva Tarde: {detalhado['horario_reserva_turno']['tarde']} (Esperado: 13:30)")
        assert detalhado["horario_reserva_turno"]["tarde"] == "13:30"
        
        # 7. Tempo médio de recepção BC (pronto 09:00, ocupou 10:00 = 60.0 min)
        print(f"Tempo Recepção BC: {detalhado['tempo_recepcao_bc_minutos']} min (Esperado: 60.0 min)")
        assert detalhado["tempo_recepcao_bc_minutos"] == 60.0

        # 8. Tempo médio de acomodação de alta (solicitado 12:00, NIR destino 14:00 = 2.0h)
        print(f"Tempo Acomodação Alta: {detalhado['tempo_acomodacao_alta_horas']}h (Esperado: 2.0h)")
        assert detalhado["tempo_acomodacao_alta_horas"] == 2.0

        # 9. Tempo médio de liberação de leito pós-UTI (destino 14:00, censo alta 15:00 = 1.0h)
        print(f"Tempo Liberação Leito Pós-UTI: {detalhado['tempo_liberacao_leito_horas']}h (Esperado: 1.0h)")
        assert detalhado["tempo_liberacao_leito_horas"] == 1.0

        print("\nTodos os testes de indicadores de fluxo passaram com sucesso! [OK]")

if __name__ == "__main__":
    asyncio.run(test_indicadores_fluxo())
