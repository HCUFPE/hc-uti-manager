import os
import paramiko
import re
from dotenv import load_dotenv

def main():
    load_dotenv()
    host = os.getenv("VM_HOST_HOMOLOGACAO")
    user = os.getenv("VM_USER_HOMOLOGACAO")
    secret = os.getenv("VM_PASSWORD_HOMOLOGACAO")

    print(f"Conectando à VM de Homologação {host} para restaurar o AD1...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=secret, timeout=15)
        sftp = ssh.open_sftp()
        r_env_path = "/var/app/hc-uti-manager/.env"
        
        # Ler o arquivo remoto
        with sftp.file(r_env_path, "r") as f:
            env_content = f.read().decode('utf-8', errors='ignore')
            
        # Restaurar as URLs corretas
        valid_urls = "ldap://UFPE-PVW-AD1.ebserhnet.ebserh.gov.br:389,ldap://UFPE-PVW-AD2.ebserhnet.ebserh.gov.br:389"
        env_content = re.sub(r"AD_URL=.*", f"AD_URL={valid_urls}", env_content)
        
        # Salvar o arquivo
        with sftp.file(r_env_path, "w") as f:
            f.write(env_content.encode('utf-8'))
            
        print("AD_URL de homologação restaurado para o estado saudável.")
        sftp.close()
        
        # Reiniciar o serviço
        print("Reiniciando o serviço de homologação...")
        stdin, stdout, stderr = ssh.exec_command("systemctl restart hc-uti.service")
        stdout.channel.recv_exit_status()
        print("Serviço de homologação operando normalmente!")
        
    except Exception as e:
        print("Erro na restauração:", e)
    finally:
        ssh.close()

if __name__ == '__main__':
    main()
