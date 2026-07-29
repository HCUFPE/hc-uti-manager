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
        
        # Buscar eventos de histórico para o prontuário 21036074
        query = "select id, tipo, acao, criado_em, detalhes from historico_acoes where prontuario='21036074';"
        cmd = f"export XDG_RUNTIME_DIR=/run/user/$(id -u) && podman exec hc-uti-backend sqlite3 /app/data/app.db \"{query}\""
        
        stdin, stdout, stderr = ssh.exec_command(cmd)
        print("History Events:")
        print(stdout.read().decode('utf-8'))
            
    except Exception as e:
        print("Error:", e)
    finally:
        ssh.close()

if __name__ == '__main__':
    main()
