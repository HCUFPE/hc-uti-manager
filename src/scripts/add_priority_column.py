import sqlite3
import os

db_path = os.path.join(os.getcwd(), 'data', 'app.db')

if not os.path.exists(db_path):
    print(f"Erro: Banco de dados não encontrado em {db_path}")
    exit(1)

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Verifica se a coluna já existe
    cursor.execute("PRAGMA table_info(solicitacoes_leito)")
    columns = [column[1] for column in cursor.fetchall()]
    
    if 'prioridade' not in columns:
        print("Adicionando coluna 'prioridade' na tabela solicitacoes_leito...")
        cursor.execute("ALTER TABLE solicitacoes_leito ADD COLUMN prioridade VARCHAR(10)")
        conn.commit()
        print("Coluna adicionada com sucesso!")
    else:
        print("A coluna 'prioridade' já existe.")
        
    conn.close()
except Exception as e:
    print(f"Erro ao atualizar banco: {e}")
