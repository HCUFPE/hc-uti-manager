import os
import paramiko
import json
from dotenv import load_dotenv

def run_query():
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
import json

conn = sqlite3.connect('/app/data/app.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()
try:
    cursor.execute("SELECT id, operador, tipo, acao, detalhes, criado_em, prontuario FROM historico_acoes WHERE prontuario IN ('22273189', '22198642') ORDER BY id DESC LIMIT 20")
    rows = [dict(r) for r in cursor.fetchall()]
    print(json.dumps(rows, default=str))
except Exception as e:
    print(json.dumps({"error": str(e)}))
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
    res = run_query()
    try:
        data = json.loads(res)
        print(json.dumps(data, indent=2, ensure_ascii=False))
    except Exception as e:
        print("Raw output:", res)
