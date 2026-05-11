import sqlite3
import os

def migrate():
    db_path = os.path.join("data", "app.db")
    if not os.path.exists(db_path):
        print(f"Banco de dados não encontrado em {db_path}")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Verifica se a coluna já existe
        cursor.execute("PRAGMA table_info(historico_acoes)")
        columns = [row[1] for row in cursor.fetchall()]
        
        if "prontuario" not in columns:
            print("Adicionando coluna 'prontuario' na tabela 'historico_acoes'...")
            cursor.execute("ALTER TABLE historico_acoes ADD COLUMN prontuario TEXT")
            conn.commit()
            print("Migração concluída com sucesso!")
        else:
            print("A coluna 'prontuario' já existe. Nada a fazer.")
            
    except Exception as e:
        print(f"Erro durante a migração: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
