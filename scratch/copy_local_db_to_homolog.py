import os
import paramiko
from dotenv import load_dotenv

def main():
    load_dotenv()
    host = os.getenv("VM_HOST_HOMOLOGACAO")
    user = os.getenv("VM_USER_HOMOLOGACAO")
    secret = os.getenv("VM_PASSWORD_HOMOLOGACAO")

    local_root = r"c:\Users\daniel.turmina\Documents\HC-uti-manager"
    l_db = os.path.join(local_root, "data", "app.db")
    r_db = "/var/app/hc-uti-manager/data/app.db"

    if not os.path.exists(l_db):
        print(f"Erro: Banco de dados local nao encontrado em: {l_db}")
        return

    print(f"Conectando à VM de Homologação {host}...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=secret, timeout=15)
        
        # 1. Parar a stack antes de substituir o banco de dados
        print("Parando os containers em homologação...")
        stdin, stdout, stderr = ssh.exec_command("cd /var/app/hc-uti-manager && podman-compose down")
        stdout.channel.recv_exit_status()
        
        # 2. Upload do banco de dados local sobrescrevendo o remoto
        print("Fazendo upload do banco de dados local...")
        sftp = ssh.open_sftp()
        sftp.put(l_db, r_db)
        sftp.close()
        print("Banco de dados local transferido com sucesso!")
        
        # 3. Subir os containers novamente
        print("Iniciando os containers em homologação...")
        stdin, stdout, stderr = ssh.exec_command("cd /var/app/hc-uti-manager && podman-compose up -d --build")
        stdout.channel.recv_exit_status()
        print("Deploy e banco de dados restaurados com sucesso!")
        
    except Exception as e:
        print("Erro durante o processo:", e)
    finally:
        ssh.close()

if __name__ == '__main__':
    main()
