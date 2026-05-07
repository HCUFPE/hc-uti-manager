import sqlite3
import os

# Caminho exato confirmado na VM
DB_PATH = 'data/app.db'

def migrate():
    if not os.path.exists(DB_PATH):
        # Tenta um fallback caso esteja rodando de dentro da pasta scratch
        alt_path = '../data/app.db'
        if os.path.exists(alt_path):
            db_path = alt_path
        else:
            print(f"Erro: Arquivo {DB_PATH} nao encontrado!")
            return
    else:
        db_path = DB_PATH

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Nome da tabela conforme definido no modelo Python
    TABLE_NAME = "solicitacoes_leito"

    print(f"Migrando banco: {db_path} | Tabela: {TABLE_NAME}")

    cols = [
        ("turno", "TEXT DEFAULT 'Manhã'"),
        ("data_cirurgia", "TEXT"),
        ("destino", "TEXT")
    ]

    for col_name, col_type in cols:
        try:
            cursor.execute(f"ALTER TABLE {TABLE_NAME} ADD COLUMN {col_name} {col_type}")
            print(f" -> Coluna '{col_name}' adicionada.")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e).lower():
                print(f" -> Coluna '{col_name}' já existe.")
            else:
                print(f" -> Erro na coluna {col_name}: {e}")

    conn.commit()
    conn.close()
    print("Migração finalizada com sucesso!")

if __name__ == "__main__":
    migrate()
