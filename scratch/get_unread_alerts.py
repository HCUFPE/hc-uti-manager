import os
import paramiko
from dotenv import load_dotenv

def main():
    load_dotenv(r"c:\Users\daniel.turmina\Documents\HC-uti-manager\.env")
    host = os.getenv("VM_HOST")
    user = os.getenv("VM_USER")
    secret = os.getenv("VM_PASSWORD")

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(host, username=user, password=secret, timeout=15)
        
        # Selecionar todos os alertas pendentes (lido = 0)
        query = "select id, titulo, lido, lido_por, criado_em, mensagem, prontuario from alertas where lido=0;"
        cmd = f"export XDG_RUNTIME_DIR=/run/user/$(id -u) && podman exec hc-uti-backend python -c \"import sqlite3; conn = sqlite3.connect('/app/data/app.db'); [print(row) for row in conn.execute('{query}').fetchall()]; conn.close()\""
        
        stdin, stdout, stderr = ssh.exec_command(cmd)
        print("Unread Alerts in DB:")
        print(stdout.read().decode('utf-8', errors='ignore'))
            
    except Exception as e:
        print("Error:", e)
    finally:
        ssh.close()

if __name__ == '__main__':
    main()
