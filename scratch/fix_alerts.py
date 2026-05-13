import sqlite3
import os

db_path = 'data/app.db'
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("UPDATE alertas SET tipo = 'critico' WHERE tipo = 'urgente'")
    conn.commit()
    print(f"Alertas corrigidos: {cursor.rowcount}")
    conn.close()
else:
    print("Banco de dados não encontrado.")
