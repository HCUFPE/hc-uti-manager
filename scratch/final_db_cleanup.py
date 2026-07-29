import sys
import os
from sqlalchemy import delete
from datetime import datetime

# Importar o gerenciador de banco de dados da aplicação
sys.path.insert(0, '/app/src')
from resources.database import DatabaseManager
from models.alerta import Alerta

async def cleanup():
    dsn = os.getenv("SQLITE_DSN") or "sqlite+aiosqlite:////app/data/app.db"
    db = DatabaseManager(dsn)
    
    async for session in db.get_session():
        # 1. Deletar todos os alertas antigos dos 3 prontuários envolvidos nas trocas de hoje
        prontuarios_troca = ["21036074", "22307987", "13938907"]
        print(f"Deletando alertas antigos para os prontuários: {prontuarios_troca}")
        await session.execute(
            delete(Alerta).where(Alerta.prontuario.in_(prontuarios_troca))
        )
        
        # 2. Criar o alerta único para a primeira troca (para 22307987 - Heloisa)
        # Lido por andreza.bahe às 09:20
        print("Criando alerta unificado para a troca 21036074 -> 22307987...")
        alerta_heloisa = Alerta(
            tipo="aviso",
            categoria="Gargalo",
            titulo="Reserva Remanejada (Troca de Paciente)",
            mensagem="Solicitação #92 (Paciente 21036074) voltou para Pendente e o Leito 0502G foi transferido para o Paciente HELOISA SIQUEIRA FERNANDES (Prontuário 22307987) via troca de paciente.",
            prontuario="22307987",
            lido=True,
            lido_em=datetime.utcnow(),
            lido_por="andreza.bahe",
            criado_em=datetime.utcnow()
        )
        session.add(alerta_heloisa)
        
        # 3. Criar o alerta único para a segunda troca (para 13938907)
        # Lido por daniel.turmina às 09:29
        print("Criando alerta unificado para a troca 21036074 -> 13938907...")
        alerta_segundo = Alerta(
            tipo="aviso",
            categoria="Gargalo",
            titulo="Reserva Remanejada (Troca de Paciente)",
            mensagem="Solicitação #92 (Paciente 21036074) foi cancelada e o Leito 0502G foi transferido para o Paciente 13938907 via troca de paciente.",
            prontuario="13938907",
            lido=True,
            lido_em=datetime.utcnow(),
            lido_por="daniel.turmina",
            criado_em=datetime.utcnow()
        )
        session.add(alerta_segundo)
        
        await session.commit()
        print("Banco de dados limpo e unificado com sucesso!")
        
    await db.close_connection()

if __name__ == "__main__":
    import asyncio
    asyncio.run(cleanup())
