import sqlite3
import os

db_path = os.path.join('data', 'app.db')
if not os.path.exists(db_path):
    print(f"Banco de dados não encontrado em {db_path}")
else:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute("ALTER TABLE solicitacoes_leito ADD COLUMN data_cirurgia VARCHAR(20);")
        print("Coluna 'data_cirurgia' adicionada com sucesso.")
    except Exception as e:
        print(f"Aviso: {e}")
    conn.commit()
    conn.close()
