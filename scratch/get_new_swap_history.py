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
        
        # Buscar todos os eventos de histórico para o prontuário 21931076
        query = "select id, tipo, acao, criado_em, detalhes from historico_acoes where prontuario='21931076' or detalhes like '%21931076%';"
        cmd = f"export XDG_RUNTIME_DIR=/run/user/$(id -u) && podman exec hc-uti-backend python -c \"import sqlite3; conn = sqlite3.connect('/app/data/app.db'); [print(row) for row in conn.execute('{query}').fetchall()]; conn.close()\""
        
        stdin, stdout, stderr = ssh.exec_command(cmd)
        print("History Events for 21931076:")
        print(stdout.read().decode('utf-8', errors='ignore'))
            
    except Exception as e:
        print("Error:", e)
    finally:
        ssh.close()

if __name__ == '__main__':
    main()
