import sqlite3
import os
import re

def populate_prontuario():
    db_path = os.path.join("data", "app.db")
    if not os.path.exists(db_path):
        print(f"Banco de dados não encontrado em {db_path}")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        print("Buscando registros antigos para popular a coluna 'prontuario'...")
        cursor.execute("SELECT id, detalhes FROM historico_acoes WHERE prontuario IS NULL OR prontuario = ''")
        rows = cursor.fetchall()
        
        count = 0
        for row_id, detalhes in rows:
            if detalhes:
                # Procura por "Prontuário XXXXX" ou "prontuário XXXXX"
                match = re.search(r"[Pp]rontuário\s*[:#]?\s*(\d+)", detalhes)
                if match:
                    prontuario = match.group(1)
                    cursor.execute("UPDATE historico_acoes SET prontuario = ? WHERE id = ?", (prontuario, row_id))
                    count += 1
        
        conn.commit()
        print(f"Sucesso! {count} registros antigos foram atualizados com o número do prontuário.")
            
    except Exception as e:
        print(f"Erro ao popular prontuários: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    populate_prontuario()
