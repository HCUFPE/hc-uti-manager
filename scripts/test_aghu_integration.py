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
from providers.implementations.solicitacao_leito_provider import SolicitacaoLeitoProvider
from controllers.solicitacao_leito_controller import SolicitacaoLeitoController

async def test_all():
    print("Iniciando testes de integração AGHU e ordenação...")
    
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
        controller = SolicitacaoLeitoController(
            leito_provider=leito_provider,
            estado_provider=None,
            historico_provider=None,
            aghu_cirurgia_provider=None # Fará o fallback para os mocks
        )
        
        # 2. Testar consulta direta ao AGHU (via mock do controller)
        print("\n--- Testando consulta de dados no AGHU (Mock) ---")
        dados = await controller.consultar_dados_aghu("77")
        print(f"Paciente 77 localizado: {dados['nome']}")
        assert dados["nome"] == "MANOEL SEVERINO DOS SANTOS"
        assert dados["idade"] > 0
        assert dados["turno"] == "Manhã" # 08:30 é Manhã
        # Data formato retornado pela controller deve ser YYYY-MM-DD
        assert "-" in dados["data_cirurgia"]
        assert len(dados["data_cirurgia"].split("-")[0]) == 4
        print("[OK] Consulta ao AGHU OK")
        
        # 3. Testar criação de solicitação e preenchimento automático
        print("\n--- Testando criação de solicitação (paciente 77) ---")
        payload = {
            "prontuario": "77",
            "tipo": "Cirurgico",
            "prioridade": "P1"
        }
        res = await controller.criar_solicitacao(payload)
        print(f"Resultado criação: {res}")
        
        # Verificar se foi inserido no banco
        db_sols = await leito_provider.get_todas()
        assert len(db_sols) == 1
        sol = db_sols[0]
        assert sol.prontuario == "77"
        assert sol.nome == "MANOEL SEVERINO DOS SANTOS"
        assert sol.idade == dados["idade"]
        assert sol.especialidade == "CCP (CABEÇA E PESCOÇO)"
        assert sol.procedimento == "TIREOIDECTOMIA PARCIAL"
        assert sol.hora_cirurgia == "08:30"
        assert sol.turno == "Manhã"
        print("[OK] Criacao e preenchimento automatico OK")
        
        # 4. Testar ordenação cronológica e prioridades (P1, P2...)
        print("\n--- Testando ordenação de prioridade baseada na hora da cirurgia ---")
        
        # Primeiro limpamos o banco
        for s in db_sols:
            await leito_provider.deletar(s.id)
            
        hoje = "2026-05-25"
        turno = "Manhã"
        
        # Adiciona Solicitacao A (10:00)
        sol_a = await leito_provider.criar({
            "prontuario": "100",
            "nome": "Paciente 100",
            "idade": 40,
            "especialidade": "GERAL",
            "procedimento": "PROC A",
            "tipo": "Cirurgico",
            "turno": turno,
            "data_cirurgia": hoje,
            "hora_cirurgia": "10:00",
            "status": "Pendente",
            "prioridade": "P1"
        })
        
        # Sincroniza
        await controller._sincronizar_prioridades(hoje, turno)
        
        # Adiciona Solicitacao B (08:30) - Deve tomar a frente (P1) e empurrar A para P2
        sol_b = await leito_provider.criar({
            "prontuario": "101",
            "nome": "Paciente 101",
            "idade": 50,
            "especialidade": "GERAL",
            "procedimento": "PROC B",
            "tipo": "Cirurgico",
            "turno": turno,
            "data_cirurgia": hoje,
            "hora_cirurgia": "08:30",
            "status": "Pendente",
            "prioridade": "P2"
        })
        
        await controller._sincronizar_prioridades(hoje, turno)
        
        # Adiciona Solicitacao C (11:00) - Deve ser P3
        sol_c = await leito_provider.criar({
            "prontuario": "102",
            "nome": "Paciente 102",
            "idade": 60,
            "especialidade": "GERAL",
            "procedimento": "PROC C",
            "tipo": "Cirurgico",
            "turno": turno,
            "data_cirurgia": hoje,
            "hora_cirurgia": "11:00",
            "status": "Pendente",
            "prioridade": "P3"
        })
        
        await controller._sincronizar_prioridades(hoje, turno)
        
        # Buscar as solicitações e verificar prioridades atribuídas
        sols_ordenadas = await leito_provider.get_todas()
        
        dict_sols = {s.prontuario: s.prioridade for s in sols_ordenadas}
        print(f"Prioridades resultantes: {dict_sols}")
        
        assert dict_sols["101"] == "P1" # 08:30
        assert dict_sols["100"] == "P2" # 10:00
        assert dict_sols["102"] == "P3" # 11:00
        
        print("[OK] Ordenacao cronologica de inicio de cirurgia OK")
        print("\nTodos os testes passaram com sucesso! [OK]")

if __name__ == "__main__":
    asyncio.run(test_all())
