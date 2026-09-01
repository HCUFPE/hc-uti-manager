import os
import paramiko
from dotenv import load_dotenv

def main():
    load_dotenv()
    host = os.getenv("VM_HOST")
    user = os.getenv("VM_USER")
    secret = os.getenv("VM_PASSWORD")

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(host, username=user, password=secret, timeout=15)
        
        # Sequência de comandos de deploy e limpeza
        commands = [
            # 1. Descartar alterações locais na VM, buscar as tags/branches e fazer checkout do master
            "cd /var/app/hc-uti-manager && git restore . && git fetch origin && git checkout master && git pull origin master",
            
            # 2. Atualizar MOCK_BEDS para false
            "sed -i 's/MOCK_BEDS=true/MOCK_BEDS=false/g' /var/app/hc-uti-manager/.env",
            
            # 3. Remover containers antigos se existirem e reiniciar o serviço systemd
            "podman rm -f hc-uti-backend hc-uti-nginx 2>/dev/null || true",
            "systemctl restart hc-uti.service",
            # Aguarda a inicialização completa do container
            "until [ \"$(podman inspect -f '{{.State.Running}}' hc-uti-backend 2>/dev/null)\" = \"true\" ]; do echo 'Aguardando inicializacao do container...'; sleep 3; done",
            
            # 4. Executar migrações do Alembic no banco de dados de produção
            "podman exec -i hc-uti-backend alembic upgrade head"
        ]
        
        for cmd in commands:
            print(f"Executing: {cmd}")
            stdin, stdout, stderr = ssh.exec_command(cmd)
            out_str = stdout.read().decode('utf-8', errors='ignore')
            err_str = stderr.read().decode('utf-8', errors='ignore')
            
            # Safe print
            safe_out = out_str.encode('ascii', errors='replace').decode('ascii')
            safe_err = err_str.encode('ascii', errors='replace').decode('ascii')
            
            print("STDOUT:")
            print(safe_out)
            print("STDERR:")
            print(safe_err)
            
    except Exception as e:
        print("Error:", e)
    finally:
        ssh.close()

if __name__ == '__main__':
    main()
