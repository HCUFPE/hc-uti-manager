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
        # 1. Deletar todos os alertas antigos dos 3 prontuários envolvidos nas trocas de hoje
        prontuarios_troca = ["21036074", "22307987", "13938907"]
        print(f"Deletando alertas antigos para os prontuários: {prontuarios_troca}")
        await session.execute(
            delete(Alerta).where(Alerta.prontuario.in_(prontuarios_troca))
        )
        
        # Obter datas baseadas nos logs de hoje (em UTC para gravação no banco)
        hoje = datetime.utcnow()
        # Horários aproximados em UTC (06:43 local = 09:43 UTC | 07:59 local = 10:59 UTC)
        criado_1 = hoje.replace(hour=9, minute=43, second=0, microsecond=0)
        criado_2 = hoje.replace(hour=10, minute=59, second=0, microsecond=0)

        # 2. Criar o alerta único para a primeira troca (para 22307987 - Heloisa)
        # O prontuário gerador é o do Paciente A (21036074)
        print("Criando alerta unificado para a troca 21036074 -> 22307987...")
        alerta_heloisa = Alerta(
            tipo="aviso",
            categoria="Gargalo",
            titulo="Reserva Remanejada (Troca de Paciente)",
            mensagem="Solicitação #92 (Paciente A) voltou para a fila (Pendente). Motivo: Leito 0502G foi remanejado para o Paciente B (Prontuário 22307987) via troca de paciente.",
            prontuario="21036074",
            lido=True,
            lido_em=criado_1 + timedelta(hours=2, minutes=37), # 09:20 local (12:20 UTC)
            lido_por="andreza.bahe",
            criado_em=criado_1
        )
        session.add(alerta_heloisa)
        
        # 3. Criar o alerta único para a segunda troca (para 13938907)
        print("Criando alerta unificado para a troca 21036074 -> 13938907...")
        alerta_segundo = Alerta(
            tipo="aviso",
            categoria="Gargalo",
            titulo="Reserva Remanejada (Troca de Paciente)",
            mensagem="Solicitação #92 (Paciente A) voltou para a fila (Pendente). Motivo: Leito 0502G foi remanejado para o Paciente B (Prontuário 13938907) via troca de paciente.",
            prontuario="21036074",
            lido=True,
            lido_em=criado_2 + timedelta(hours=1, minutes=30), # 09:29 local (12:29 UTC)
            lido_por="daniel.turmina",
            criado_em=criado_2
        )
        session.add(alerta_segundo)
        
        await session.commit()
        print("Banco de dados limpo e unificado com sucesso!")
        
    await db.close_connection()

if __name__ == "__main__":
    import asyncio
    asyncio.run(cleanup())
