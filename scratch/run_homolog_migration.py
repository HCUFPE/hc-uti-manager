import os
import paramiko
from dotenv import load_dotenv

def main():
    load_dotenv()
    host = os.getenv("VM_HOST_HOMOLOGACAO")
    user = os.getenv("VM_USER_HOMOLOGACAO")
    secret = os.getenv("VM_PASSWORD_HOMOLOGACAO")

    print(f"Conectando à VM de homologação {host} para rodar as migrações...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=secret, timeout=15)
        stdin, stdout, stderr = ssh.exec_command("podman exec -i hc-uti-backend-homolog alembic upgrade head")
        
        output = stdout.read().decode('utf-8')
        errors = stderr.read().decode('utf-8')
        
        if output:
            print("Saída:")
            print(output)
        if errors:
            print("Erros/Log:")
            print(errors)
            
        print("Migração em Homologação concluída!")
    except Exception as e:
        print("Erro ao executar migrações na VM:", e)
    finally:
        ssh.close()

if __name__ == '__main__':
    main()
