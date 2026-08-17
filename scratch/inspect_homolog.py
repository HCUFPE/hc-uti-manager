import os
import paramiko
from dotenv import load_dotenv

def main():
    load_dotenv()
    host = os.getenv("VM_HOST_HOMOLOGACAO")
    user = os.getenv("VM_USER_HOMOLOGACAO")
    secret = os.getenv("VM_PASSWORD_HOMOLOGACAO")

    print(f"Conectando a VM de homologacao {host} como {user}...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=secret, timeout=15)
        print("Conectado com sucesso!\n")
        
        print("=== CONTAINERS ATIVOS (PODMAN) ===")
        stdin, stdout, stderr = ssh.exec_command("podman ps -a")
        print(stdout.read().decode('utf-8', errors='ignore'))
        
        print("=== PORTAS EM USO (NETSTAT/SS) ===")
        stdin, stdout, stderr = ssh.exec_command("ss -tulpn")
        print(stdout.read().decode('utf-8', errors='ignore'))
            
    except Exception as e:
        print("Erro ao conectar/inspecionar:", e)
    finally:
        ssh.close()

if __name__ == '__main__':
    main()
