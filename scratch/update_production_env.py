import os
import secrets
import paramiko
import re
from dotenv import load_dotenv

def main():
    load_dotenv()
    host = os.getenv("VM_HOST")
    user = os.getenv("VM_USER")
    secret = os.getenv("VM_PASSWORD")

    if not host or not user or not secret:
        print("Erro: Credenciais de produção não encontradas no .env local!")
        return

    print(f"Conectando à VM de Produção {host} para atualizar o .env...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=secret, timeout=15)
        sftp = ssh.open_sftp()
        
        r_env_path = "/var/app/hc-uti-manager/.env"
        
        # Ler o arquivo remoto
        print("Lendo .env remoto...")
        with sftp.file(r_env_path, "r") as f:
            env_content = f.read().decode('utf-8', errors='ignore')
            
        # Modificar o AD_URL
        print("Atualizando AD_URL...")
        novas_urls = "ldap://UFPE-PVW-AD1.ebserhnet.ebserh.gov.br:389,ldap://UFPE-PVW-AD2.ebserhnet.ebserh.gov.br:389"
        if "AD_URL=" in env_content:
            env_content = re.sub(r"AD_URL=.*", f"AD_URL={novas_urls}", env_content)
        else:
            env_content += f"\nAD_URL={novas_urls}\n"
            
        # Modificar o JWT_SECRET com uma chave robusta e exclusiva para Produção
        print("Gerando e atualizando JWT_SECRET de produção...")
        novo_jwt = secrets.token_hex(32)
        if "JWT_SECRET=" in env_content:
            env_content = re.sub(r"JWT_SECRET=.*", f"JWT_SECRET={novo_jwt}", env_content)
        else:
            env_content += f"\nJWT_SECRET={novo_jwt}\n"
            
        # Salvar o arquivo atualizado
        with sftp.file(r_env_path, "w") as f:
            f.write(env_content.encode('utf-8'))
            
        print("Arquivo .env de produção atualizado com sucesso!")
        sftp.close()
    except Exception as e:
        print("Erro ao atualizar o .env na VM de produção:", e)
    finally:
        ssh.close()

if __name__ == '__main__':
    main()
