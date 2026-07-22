import os
import paramiko
import json
from dotenv import load_dotenv

def run_fix_script():
    load_dotenv()
    host = os.getenv("VM_HOST")
    user = os.getenv("VM_USER")
    secret = os.getenv("VM_PASSWORD")

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(host, username=user, password=secret, timeout=15)
        
        # We will write a python script that will run inside the container to perform the update
        py_code = """
import sqlite3
import json

conn = sqlite3.connect('/app/data/app.db')
cursor = conn.cursor()
try:
    # 1. Update solicitation 18 to Concluída
    cursor.execute("UPDATE solicitacoes_leito SET status = 'Concluída', atualizado_em = '2026-07-14 22:18:40' WHERE id = 18")
    print(f"Updated solicitacoes_leito: {cursor.rowcount} rows affected.")
    
    # 2. Insert conclusao event in historico_acoes
    cursor.execute(
        "INSERT INTO historico_acoes (operador, tipo, acao, detalhes, prontuario, criado_em) VALUES (?, ?, ?, ?, ?, ?)",
        (
            "Sistema (Censo)",
            "conclusao",
            "Admissão concluída no leito 0502K",
            "Paciente ocupou o leito 0502K. Solicitação #18 concluída automaticamente via censo.",
            "16309536",
            "2026-07-14 22:18:40.000000"
        )
    )
    print(f"Inserted into historico_acoes: {cursor.rowcount} rows affected.")
    conn.commit()
    print("Database changes committed successfully.")
except Exception as e:
    conn.rollback()
    print("Database error:", e)
finally:
    conn.close()
"""
        cmd = "podman exec -i hc-uti-backend python"
        print("Executing script on remote container...")
        stdin, stdout, stderr = ssh.exec_command(cmd)
        stdin.write(py_code)
        stdin.flush()
        stdin.channel.shutdown_write()
        
        out = stdout.read().decode('utf-8', errors='ignore')
        err = stderr.read().decode('utf-8', errors='ignore')
        
        if err:
            print("STDERR:", err)
        print("STDOUT:")
        print(out)
    except Exception as e:
        print("Error during SSH execution:", e)
    finally:
        ssh.close()

if __name__ == '__main__':
    run_fix_script()
