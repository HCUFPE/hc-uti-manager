import os
import paramiko
import json
from dotenv import load_dotenv

def run_update():
    load_dotenv()
    host = os.getenv("VM_HOST")
    user = os.getenv("VM_USER")
    secret = os.getenv("VM_PASSWORD")

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(host, username=user, password=secret, timeout=15)
        
        py_code = """
import sqlite3

conn = sqlite3.connect('/app/data/app.db')
cursor = conn.cursor()
try:
    # 1. Update entry 81 details to "Alteração de Prioridade pós Solicitação"
    cursor.execute(
        "UPDATE historico_acoes SET detalhes = ? WHERE id = ?",
        ["Solicitação #5 (Prontuário 22273189) - Motivo: Alteração de Prioridade pós Solicitação", 81]
    )
    print("Updated history entry 81 details.")

    # 2. Update entry 97 operator to "Sistema"
    cursor.execute(
        "UPDATE historico_acoes SET operador = ? WHERE id = ?",
        ["Sistema", 97]
    )
    print("Updated history entry 97 operator to Sistema.")

    conn.commit()
except Exception as e:
    print("Error:", str(e))
    conn.rollback()
finally:
    conn.close()
"""
        cmd = "podman exec -i hc-uti-backend python"
        stdin, stdout, stderr = ssh.exec_command(cmd)
        stdin.write(py_code)
        stdin.flush()
        stdin.channel.shutdown_write()
        
        out = stdout.read().decode('utf-8', errors='ignore')
        return out
    except Exception as e:
        print("Error:", e)
        return None
    finally:
        ssh.close()

if __name__ == "__main__":
    res = run_update()
    print("Output:", res)
