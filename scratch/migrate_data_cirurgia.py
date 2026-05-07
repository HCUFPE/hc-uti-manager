import sqlite3
import os

# Caminho para o banco de dados SQLite na VM
DB_PATH = 'solicitacoes.db'

def migrate():
    if not os.path.exists(DB_PATH):
        print(f"Banco {DB_PATH} nao encontrado. Pulando migracao.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Nome da tabela conforme definido em src/models/solicitacao_leito.py
    TABLE_NAME = "solicitacoes_leito"

    print(f"Iniciando migracao na tabela: {TABLE_NAME}")

    cols_to_add = [
        ("turno", "TEXT DEFAULT 'Manha'"),
        ("data_cirurgia", "TEXT"),
        ("destino", "TEXT")
    ]

    for col_name, col_type in cols_to_add:
        try:
            cursor.execute(f"ALTER TABLE {TABLE_NAME} ADD COLUMN {col_name} {col_type}")
            print(f"Coluna '{col_name}' adicionada com sucesso.")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e).lower():
                print(f"Coluna '{col_name}' ja existe. Ignorado.")
            else:
                print(f"Erro ao adicionar coluna {col_name}: {e}")

    conn.commit()
    conn.close()
    print("Migracao concluida.")

if __name__ == "__main__":
    migrate()
