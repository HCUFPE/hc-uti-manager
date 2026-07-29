import sys
import os
from sqlalchemy import select

# Importar o gerenciador de banco de dados da aplicação
sys.path.insert(0, '/app/src')
from resources.database import DatabaseManager
from models.alerta import Alerta

async def verify():
    dsn = os.getenv("SQLITE_DSN") or "sqlite+aiosqlite:////app/data/app.db"
    db = DatabaseManager(dsn)
    
    async for session in db.get_session():
        res = await session.execute(select(Alerta).order_by(Alerta.id.desc()))
        alertas = res.scalars().all()
        
        print("=== RELATORIO GERAL DE ALERTAS NO BANCO ===")
        print(f"Total de alertas cadastrados: {len(alertas)}")
        
        # 1. Verificar duplicidades exatas (mesmo titulo, mensagem e prontuario)
        print("\n1. Checagem de Duplicidades Exatas:")
        seen = {}
        duplicates = []
        for a in alertas:
            key = (a.titulo, a.mensagem, a.prontuario)
            if key in seen:
                duplicates.append((a.id, seen[key], key))
            else:
                seen[key] = a.id
                
        if duplicates:
            print(f"[!] Alerta: Encontrados {len(duplicates)} alertas duplicados!")
            for dup_id, orig_id, key in duplicates:
                print(f"  - ID Duplicado: {dup_id} | ID Original: {orig_id} | Chave: {key[0]} - Pront: {key[2]}")
        else:
            print("[OK] Sucesso: Nenhuma duplicidade exata encontrada no banco de dados.")
            
        # 2. Verificar estado dos alertas referentes às trocas de hoje
        print("\n2. Checagem dos Alertas de Trocas de Hoje:")
        prontuarios_troca = ["21036074", "22307987", "13938907"]
        alertas_hoje = [a for a in alertas if a.prontuario in prontuarios_troca]
        
        if alertas_hoje:
            for a in alertas_hoje:
                print(f"  - ID: {a.id} | Titulo: {a.titulo} | Lido: {a.lido} | Por: {a.lido_por} | Msg: {a.mensagem[:100]}...")
        else:
            print("[!] Nenhum alerta encontrado para os prontuarios das trocas.")
            
    await db.close_connection()

if __name__ == "__main__":
    import asyncio
    asyncio.run(verify())
