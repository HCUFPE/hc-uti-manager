import sys
import os
import asyncio

# Adiciona o diretório 'src' ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from resources.database import Base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from models.solicitacao_leito import SolicitacaoLeito
from models.leito_estado import LeitoEstado
from models.historico_acao import HistoricoAcao
from providers.implementations.solicitacao_leito_provider import SolicitacaoLeitoProvider
from providers.implementations.leito_estado_provider import LeitoEstadoProvider
from providers.implementations.historico_provider import HistoricoProvider
from controllers.solicitacao_leito_controller import SolicitacaoLeitoController

async def test_historico_edicao():
    print("Iniciando testes de histórico de edição e troca de paciente...")
    
    # 1. Configurar banco SQLite temporário em memória
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session() as session:
        # Instanciar provedores e controller
        leito_provider = SolicitacaoLeitoProvider(session=session)
        estado_provider = LeitoEstadoProvider(session=session)
        historico_provider = HistoricoProvider(session=session)
        
        controller = SolicitacaoLeitoController(
            leito_provider=leito_provider,
            estado_provider=estado_provider,
            historico_provider=historico_provider,
            aghu_cirurgia_provider=None # Fará o fallback para os mocks
        )
        
        # Inicializa o LeitoEstado para podermos reservar leitos
        leito_estado = LeitoEstado(lto_id="UTI-01")
        session.add(leito_estado)
        await session.commit()

        # 2. Criar uma solicitação inicial (paciente 77)
        print("\n--- Criando solicitação inicial (Prontuário 77) ---")
        payload = {
            "prontuario": "77",
            "tipo": "Cirurgico",
            "prioridade": "P1"
        }
        await controller.criar_solicitacao(payload)
        
        # Buscar solicitação criada
        db_sols = await leito_provider.get_todas()
        assert len(db_sols) == 1
        sol_original = db_sols[0]
        assert sol_original.prontuario == "77"
        assert sol_original.status == "Pendente"
        print(f"[OK] Solicitação original ID: {sol_original.id} criada.")

        # 3. Reservar leito UTI-01 para a solicitação original
        print("\n--- Reservando leito UTI-01 para a solicitação original ---")
        res_reserva = await controller.reservar_leito(sol_original.id, "UTI-01")
        print(f"Resultado reserva: {res_reserva}")
        
        # Verificar estado após reserva
        await session.refresh(sol_original)
        assert sol_original.status == "Reservado"
        assert sol_original.destino == "Leito UTI-01"
        
        # Verificar leito físico
        res_estado = await session.execute(select(LeitoEstado).where(LeitoEstado.lto_id == "UTI-01"))
        estado_fisico = res_estado.scalar_one()
        assert estado_fisico.solicitacao_id == sol_original.id
        assert estado_fisico.prontuario_proximo == 77
        print("[OK] Reserva efetuada com sucesso no leito físico.")

        # 4. Editar solicitação, alterando o prontuário para 123 (Troca de Paciente)
        print("\n--- Editando a solicitação (Alterando Prontuário 77 -> 123) ---")
        payload_edicao = {
            "prontuario": "123",
            "tipo": "Cirurgico",
            "prioridade": "P1"
        }
        res_edicao = await controller.editar_solicitacao(
            sol_id=sol_original.id,
            payload=payload_edicao,
            user_perfil="BC",
            username="Dr. Carlos"
        )
        print(f"Resultado edição: {res_edicao}")
        
        # Recarregar banco e verificar transição
        await session.refresh(sol_original)
        
        # A solicitação original deve estar cancelada e sem destino
        assert sol_original.status == "Cancelada"
        assert sol_original.destino is None
        
        # Como get_todas() filtra solicitações canceladas, ele deve retornar apenas 1 (a nova)
        active_sols = await leito_provider.get_todas()
        print(f"Active sols: {[s.id for s in active_sols]}")
        assert len(active_sols) == 1
        assert active_sols[0].prontuario == "123"
        
        # Para verificar todas (incluindo as canceladas), consultamos o banco diretamente
        res_db = await session.execute(select(SolicitacaoLeito))
        sols_todas = list(res_db.scalars().all())
        print(f"All sols in DB: {[(s.id, s.prontuario, s.status, s.destino) for s in sols_todas]}")
        # Deve ter 2 no total (original cancelada e nova reservada)
        assert len(sols_todas) == 2
        
        nova_sol = next((s for s in sols_todas if s.id != sol_original.id), None)
        assert nova_sol is not None
        assert nova_sol.prontuario == "123"
        assert nova_sol.status == "Reservado"
        assert nova_sol.destino == "Leito UTI-01"
        assert nova_sol.nome == "ANA MARIA SILVA" # Nome do prontuário 123 no mock
        
        # O leito físico deve agora apontar para a nova solicitação e novos dados do paciente 123
        await session.refresh(estado_fisico)
        print(f"Estado Fisico UTI-01: ID={estado_fisico.lto_id}, SolicitacaoID={estado_fisico.solicitacao_id}, ProntuarioProximo={estado_fisico.prontuario_proximo}")
        
        # Let's query it freshly from DB
        res_estado_fresh = await session.execute(select(LeitoEstado).where(LeitoEstado.lto_id == "UTI-01"))
        estado_fisico_fresh = res_estado_fresh.scalar_one()
        print(f"Fresh Estado Fisico UTI-01: ID={estado_fisico_fresh.lto_id}, SolicitacaoID={estado_fisico_fresh.solicitacao_id}, ProntuarioProximo={estado_fisico_fresh.prontuario_proximo}")

        assert estado_fisico.solicitacao_id == nova_sol.id
        assert estado_fisico.prontuario_proximo == 123
        assert estado_fisico.especialidade_proximo == "TORÁCICA"
        print("[OK] Troca de paciente e portabilidade da reserva no leito físico efetuadas perfeitamente.")

        # 5. Validar logs do histórico de ações gravados
        print("\n--- Validando logs do histórico de ações ---")
        historico_logs = await historico_provider.listar(limit=100)
        
        # Deve ter registrado pelo menos:
        # - Reserva inicial (operador Sistema/current_user de quando reservou - aqui no teste foi passador default "Sistema" ou current_user)
        # - Cancelamento da original (operador Dr. Carlos, motivo contendo "Alteração de Prioridade pós Reserva de Leito")
        # - Nova solicitação criada (operador Dr. Carlos)
        # - Transferência/reserva da nova solicitação no leito físico (operador Dr. Carlos)
        
        # Vamos imprimir e analisar
        for log in reversed(historico_logs):
            print(f"Log: [{log['criado_em']}] Operador: {log['operador']} | Ação: {log['acao']} | Detalhes: {log['detalhes']}")
            
        # Filtra os logs gerados pelo operador "Dr. Carlos"
        logs_carlos = [l for l in historico_logs if l["operador"] == "Dr. Carlos"]
        assert len(logs_carlos) >= 3
        
        # Log de cancelamento
        log_cancelamento = next((l for l in logs_carlos if l["tipo"] == "exclusao_solicitacao"), None)
        assert log_cancelamento is not None
        assert "Alteração de Prioridade pós Reserva de Leito" in log_cancelamento["detalhes"]
        assert log_cancelamento["prontuario"] == "77"
        
        # Log de criação
        log_criacao = next((l for l in logs_carlos if l["tipo"] == "nova_solicitacao"), None)
        assert log_criacao is not None
        assert "gerada via troca de paciente" in log_criacao["detalhes"].lower()
        assert log_criacao["prontuario"] == "123"
        
        # Log de reserva do leito UTI-01 transferido
        log_reserva = next((l for l in logs_carlos if l["tipo"] == "reserva"), None)
        assert log_reserva is not None
        assert "UTI-01" in log_reserva["detalhes"]
        assert log_reserva["prontuario"] == "123"
        
        print("[OK] Logs de auditoria no histórico de ações validados com sucesso.")
        print("\nTodos os testes de histórico e troca de paciente passaram! [OK]")

if __name__ == "__main__":
    asyncio.run(test_historico_edicao())
