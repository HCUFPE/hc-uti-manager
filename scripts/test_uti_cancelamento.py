import sys
import os
import asyncio
from fastapi import HTTPException

# Adiciona o diretório 'src' ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from resources.database import Base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from models.solicitacao_leito import SolicitacaoLeito
from models.historico_acao import HistoricoAcao
from providers.implementations.solicitacao_leito_provider import SolicitacaoLeitoProvider
from providers.implementations.historico_provider import HistoricoProvider
from controllers.solicitacao_leito_controller import SolicitacaoLeitoController
from routers.solicitacoes_leito import cancelar_solicitacao

async def test_uti_cancelamento():
    print("Iniciando testes de cancelamento de solicitação pela UTI...")
    
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
        historico_provider = HistoricoProvider(session=session)
        controller = SolicitacaoLeitoController(
            leito_provider=leito_provider,
            estado_provider=None,
            historico_provider=historico_provider,
            aghu_cirurgia_provider=None
        )
        
        # 2. Criar solicitação de teste criada pelo Bloco Cirúrgico (BC)
        print("\n--- Criando solicitação pendente criada pelo BC ---")
        sol = await leito_provider.criar({
            "prontuario": "77",
            "nome": "MANOEL SEVERINO DOS SANTOS",
            "idade": 99,
            "especialidade": "GERAL",
            "procedimento": "TIREOIDECTOMIA",
            "tipo": "Cirurgico",
            "turno": "Manhã",
            "data_cirurgia": "2026-05-26",
            "hora_cirurgia": "08:30",
            "status": "Pendente",
            "perfil_solicitante": "BC"
        })
        print(f"[OK] Solicitação ID: {sol.id} criada.")

        # Teste 3.1: Usuário da UTI tenta cancelar com motivo inválido (ex: "Outro")
        print("\n--- Teste 3.1: UTI tentando cancelar com motivo qualquer (deve ser bloqueado) ---")
        user_uti = {
            "username": "enf_uti_1",
            "perfil": "UTI"
        }
        
        try:
            await cancelar_solicitacao(
                sol_id=sol.id,
                motivo="Alteração do mapa cirúrgico",
                controller=controller,
                historico=historico_provider,
                current_user=user_uti
            )
            assert False, "Deveria ter lançado HTTPException(403)"
        except HTTPException as e:
            assert e.status_code == 403
            print(f"[OK] Bloqueado corretamente com status {e.status_code}: {e.detail}")

        # Teste 3.2: Usuário de outro setor (COB) tenta cancelar solicitação do BC (deve ser bloqueado)
        print("\n--- Teste 3.2: Usuário do COB tentando cancelar solicitação do BC (deve ser bloqueado) ---")
        user_cob = {
            "username": "enf_cob_1",
            "perfil": "COB"
        }
        
        try:
            await cancelar_solicitacao(
                sol_id=sol.id,
                motivo="Falta de vaga de UTI",
                controller=controller,
                historico=historico_provider,
                current_user=user_cob
            )
            assert False, "Deveria ter lançado HTTPException(403)"
        except HTTPException as e:
            assert e.status_code == 403
            print(f"[OK] Bloqueado corretamente com status {e.status_code}: {e.detail}")

        # Teste 3.3: Usuário da UTI cancela com o motivo correto "Falta de vaga de UTI" (deve funcionar)
        print("\n--- Teste 3.3: UTI cancelando com motivo 'Falta de vaga de UTI' (deve funcionar) ---")
        res_cancel = await cancelar_solicitacao(
            sol_id=sol.id,
            motivo="Falta de vaga de UTI",
            controller=controller,
            historico=historico_provider,
            current_user=user_uti
        )
        print(f"Resultado do cancelamento: {res_cancel}")
        
        # Verificar estado no banco
        await session.refresh(sol)
        assert sol.status == "Cancelada"
        print("[OK] Solicitação cancelada e status atualizado para 'Cancelada'.")
        
        # Verificar histórico
        historico_logs = await historico_provider.listar(limit=1)
        assert len(historico_logs) == 1
        log = historico_logs[0]
        assert log["operador"] == "enf_uti_1"
        assert log["tipo"] == "exclusao_solicitacao"
        assert "Falta de vaga de UTI" in log["detalhes"]
        print("[OK] Histórico gravado corretamente com o motivo e o operador da UTI.")

        # Teste 3.4: UTI tentando cancelar solicitação já reservada (deve ser bloqueado)
        print("\n--- Teste 3.4: Criando solicitação Reservada e UTI tentando cancelar (deve ser bloqueado) ---")
        sol_reservada = await leito_provider.criar({
            "prontuario": "123",
            "nome": "ANA MARIA SILVA",
            "idade": 30,
            "especialidade": "GERAL",
            "procedimento": "PROC",
            "tipo": "Cirurgico",
            "turno": "Manhã",
            "data_cirurgia": "2026-05-26",
            "hora_cirurgia": "08:30",
            "status": "Reservado",
            "destino": "Leito UTI-02",
            "perfil_solicitante": "BC"
        })
        
        try:
            await cancelar_solicitacao(
                sol_id=sol_reservada.id,
                motivo="Falta de vaga de UTI",
                controller=controller,
                historico=historico_provider,
                current_user=user_uti
            )
            assert False, "Deveria ter lançado HTTPException(403) para status Reservado"
        except HTTPException as e:
            assert e.status_code == 403
            print(f"[OK] Bloqueado corretamente para cancelamento direto de vaga reservada: {e.detail}")

    print("\nTodos os testes de cancelamento pela UTI passaram com sucesso! [OK]")

if __name__ == "__main__":
    asyncio.run(test_uti_cancelamento())
