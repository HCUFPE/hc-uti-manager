import os
import paramiko
from dotenv import load_dotenv

def download_prod_db():
    load_dotenv()
    prod_host = os.getenv("VM_HOST", "10.34.0.192")
    prod_user = os.getenv("VM_USER", "root")
    prod_pass = os.getenv("VM_PASSWORD", "hc*l0ck2025")
    
    local_db = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "app.db"))
    os.makedirs(os.path.dirname(local_db), exist_ok=True)

    print(f"1. Conectando à VM de Produção ({prod_host}) para baixar o banco atual...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(prod_host, username=prod_user, password=prod_pass, timeout=15)
        sftp = ssh.open_sftp()
        remote_db = "/var/app/hc-uti-manager/data/app.db"
        print(f"Baixando {remote_db} para {local_db}...")
        sftp.get(remote_db, local_db)
        sftp.close()
        print("Banco de Produção baixado localmente com sucesso!")
    except Exception as e:
        print("Erro ao baixar banco da Produção:", e)
        raise e
    finally:
        ssh.close()

def upload_homolog_db():
    load_dotenv()
    homolog_host = os.getenv("VM_HOST_HOMOLOGACAO", "10.34.0.151")
    homolog_user = os.getenv("VM_USER_HOMOLOGACAO", "root")
    homolog_pass = os.getenv("VM_PASSWORD_HOMOLOGACAO", "hc*l0ck2026")
    
    local_db = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "app.db"))

    print(f"3. Conectando à VM de Homologação ({homolog_host}) para enviar o banco migrado...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(homolog_host, username=homolog_user, password=homolog_pass, timeout=15)
        sftp = ssh.open_sftp()
        remote_db = "/var/app/hc-uti-manager/data/app.db"
        
        # Parar containers temporariamente para evitar travar o arquivo SQLite
        print("Parando container de homologação para evitar locks no SQLite...")
        ssh.exec_command("cd /var/app/hc-uti-manager && podman-compose stop")
        
        print(f"Enviando {local_db} para {remote_db}...")
        sftp.put(local_db, remote_db)
        sftp.close()
        
        # Subir containers novamente
        print("Reiniciando containers de homologação...")
        ssh.exec_command("cd /var/app/hc-uti-manager && podman-compose start")
        print("Banco de dados atualizado e migrado enviado com sucesso para Homologação!")
    except Exception as e:
        print("Erro ao enviar banco para Homologação:", e)
        raise e
    finally:
        ssh.close()

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "upload":
        upload_homolog_db()
    else:
        download_prod_db()
