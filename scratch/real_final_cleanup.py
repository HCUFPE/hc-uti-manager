import sys
import os
from sqlalchemy import delete
from datetime import datetime, timedelta

# Importar o gerenciador de banco de dados da aplicação
sys.path.insert(0, '/app/src')
from resources.database import DatabaseManager
from models.alerta import Alerta

async def cleanup():
    dsn = os.getenv("SQLITE_DSN") or "sqlite+aiosqlite:////app/data/app.db"
    db = DatabaseManager(dsn)
    
    async for session in db.get_session():
        # 1. Deletar todos os alertas dos 3 prontuários envolvidos nas trocas
        prontuarios_troca = ["21036074", "22307987", "13938907"]
        print(f"Deletando alertas para prontuários: {prontuarios_troca}")
        await session.execute(
            delete(Alerta).where(Alerta.prontuario.in_(prontuarios_troca))
        )
        
        # 2. Criar alerta 1 (troca para 22307987)
        # O prontuário gerador é o 21036074, para que o motor encontre a correspondência perfeita de chave
        print("Criando alerta unificado para a troca -> 22307987...")
        alerta_1 = Alerta(
            tipo="aviso",
            categoria="Gargalo",
            titulo="Reserva Remanejada (Troca de Paciente)",
            mensagem="Solicitação #92 (Paciente A) voltou para a fila (Pendente). Motivo: Leito 0502G foi remanejado para o Paciente B (Prontuário 22307987) via troca de paciente.",
            prontuario="21036074",
            lido=True,
            lido_em=datetime.utcnow(),
            lido_por="Sistema",
            criado_em=datetime.utcnow() - timedelta(hours=3)
        )
        session.add(alerta_1)
        
        # 3. Criar alerta 2 (troca para 13938907)
        print("Criando alerta unificado para a troca -> 13938907...")
        alerta_2 = Alerta(
            tipo="aviso",
            categoria="Gargalo",
            titulo="Reserva Remanejada (Troca de Paciente)",
            mensagem="Solicitação #92 (Paciente A) voltou para a fila (Pendente). Motivo: Leito 0502G foi remanejado para o Paciente B (Prontuário 13938907) via troca de paciente.",
            prontuario="21036074",
            lido=True,
            lido_em=datetime.utcnow(),
            lido_por="Sistema",
            criado_em=datetime.utcnow() - timedelta(hours=2)
        )
        session.add(alerta_2)
        
        await session.commit()
        print("Finalização da limpeza executada com sucesso!")
        
    await db.close_connection()

if __name__ == "__main__":
    import asyncio
    asyncio.run(cleanup())
