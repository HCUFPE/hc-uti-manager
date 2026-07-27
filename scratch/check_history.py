import os
import paramiko
from dotenv import load_dotenv

def main():
    load_dotenv()
    host = os.getenv("VM_HOST")
    user = os.getenv("VM_USER")
    secret = os.getenv("VM_PASSWORD")

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(host, username=user, password=secret, timeout=15)
        
        # Query matching history actions via Python inside the container
        cmd = "podman exec hc-uti-backend python -c \"" \
              "import sqlite3; " \
              "conn = sqlite3.connect('/app/data/app.db'); " \
              "cursor = conn.cursor(); " \
              "cursor.execute('SELECT id, operador, tipo, acao, detalhes, prontuario, criado_em FROM historico_acoes WHERE prontuario = \"22226740\" ORDER BY criado_em ASC;'); " \
              "rows = cursor.fetchall(); " \
              "print(list(rows))\""
        print(f"Executing: {cmd}")
        stdin, stdout, stderr = ssh.exec_command(cmd)
        print("STDOUT:")
        print(stdout.read().decode('utf-8', errors='ignore'))
        print("STDERR:")
        print(stderr.read().decode('utf-8', errors='ignore'))
        
    except Exception as e:
        print("Error:", e)
    finally:
        ssh.close()

if __name__ == '__main__':
    main()
