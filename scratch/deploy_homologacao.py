import os
import paramiko
from dotenv import load_dotenv

def main():
    load_dotenv()
    host = os.getenv("VM_HOST_HOMOLOGACAO")
    user = os.getenv("VM_USER_HOMOLOGACAO")
    secret = os.getenv("VM_PASSWORD_HOMOLOGACAO")

    if not host or not user or not secret:
        print("Erro: As variáveis de ambiente VM_HOST_HOMOLOGACAO, VM_USER_HOMOLOGACAO e VM_PASSWORD_HOMOLOGACAO devem estar configuradas no arquivo .env")
        return

    print(f"Conectando à VM de Homologação ({host}) como '{user}'...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(host, username=user, password=secret, timeout=15)
        print("Conexão SSH estabelecida com sucesso!")
        
        # Sequência de comandos de deploy para a branch homologacao
        commands = [
            # 1. Descartar alterações locais na VM, buscar e fazer checkout de homologacao
            "cd /var/app/hc-uti-manager && git restore . && git fetch origin && git checkout homologacao && git pull origin homologacao",
            
            # 2. Reconstruir imagem podman (se aplicável)
            "cd /var/app/hc-uti-manager && podman build --no-cache -t localhost/hc-uti-manager_backend:latest . 2>&1 || true",
            
            # 3. Remover containers antigos se existirem e reiniciar o serviço systemd
            "podman rm -f hc-uti-backend hc-uti-nginx 2>/dev/null || true",
            "systemctl restart hc-uti.service 2>/dev/null || systemctl restart hc-uti-manager.service 2>/dev/null || true",
            
            # 4. Aguarda a inicialização completa do container
            "until [ \"$(podman inspect -f '{{.State.Running}}' hc-uti-backend 2>/dev/null)\" = \"true\" ]; do echo 'Aguardando inicialização do container...'; sleep 3; done",
            
            # 5. Executar migrações do Alembic se houver
            "podman exec -i hc-uti-backend alembic upgrade head 2>&1 || true"
        ]
        
        for cmd in commands:
            print(f"\nExecutando: {cmd}")
            stdin, stdout, stderr = ssh.exec_command(cmd)
            out_str = stdout.read().decode('utf-8', errors='ignore')
            err_str = stderr.read().decode('utf-8', errors='ignore')
            
            safe_out = out_str.encode('ascii', errors='replace').decode('ascii')
            safe_err = err_str.encode('ascii', errors='replace').decode('ascii')
            
            if safe_out:
                print("STDOUT:")
                print(safe_out)
            if safe_err:
                print("STDERR:")
                print(safe_err)
                
        print("\nDeploy em Homologação concluído com sucesso!")
            
    except Exception as e:
        print("Erro durante o deploy:", e)
    finally:
        ssh.close()

if __name__ == '__main__':
    main()
