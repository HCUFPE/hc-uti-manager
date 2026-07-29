import sys
import os
from sqlalchemy import delete
from datetime import datetime

# Importar o gerenciador de banco de dados da aplicação
sys.path.insert(0, '/app/src')
from resources.database import DatabaseManager
from models.alerta import Alerta

async def run_precise_fix():
    dsn = os.getenv("SQLITE_DSN") or "sqlite+aiosqlite:////app/data/app.db"
    db = DatabaseManager(dsn)
    
    async for session in db.get_session():
        # 1. Limpar todos os alertas desses prontuários
        prontuarios_troca = ["21036074", "22307987", "13938907"]
        print(f"Limpando alertas para prontuários: {prontuarios_troca}")
        await session.execute(
            delete(Alerta).where(Alerta.prontuario.in_(prontuarios_troca))
        )
        
        # 2. Inserir o Alerta da troca da Heloísa (22307987) com o timestamp exato do histórico
        print("Inserindo alerta unificado exato para Heloísa...")
        alerta_1 = Alerta(
            tipo="aviso",
            categoria="Gargalo",
            titulo="Reserva Remanejada (Troca de Paciente)",
            mensagem="Solicitação #92 (Prontuário 21036074) voltou para Pendente devido à troca de paciente (Prontuário 21036074 foi substituído pelo Prontuário 22307987) (Mesclado)",
            prontuario="21036074",
            lido=True,
            lido_em=datetime.utcnow(),
            lido_por="Sistema",
            criado_em=datetime.fromisoformat("2026-07-29 09:43:07.569957")
        )
        session.add(alerta_1)
        
        # 3. Inserir o Alerta da troca do prontuário 13938907 com o timestamp exato do histórico
        print("Inserindo alerta unificado exato para prontuário 13938907...")
        alerta_2 = Alerta(
            tipo="aviso",
            categoria="Gargalo",
            titulo="Reserva Remanejada (Troca de Paciente)",
            mensagem="Solicitação #92 (Prontuário 21036074) voltou para Pendente devido à troca de paciente (Prontuário 21036074 foi substituído pelo Prontuário 13938907) (Mesclado)",
            prontuario="21036074",
            lido=True,
            lido_em=datetime.utcnow(),
            lido_por="Sistema",
            criado_em=datetime.fromisoformat("2026-07-29 10:59:05.951300")
        )
        session.add(alerta_2)
        
        await session.commit()
        print("Ajuste de alertas com precisão de milissegundos concluído!")
        
    await db.close_connection()

if __name__ == "__main__":
    import asyncio
    asyncio.run(run_precise_fix())
