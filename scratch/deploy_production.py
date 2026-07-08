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
            # 1. Puxar o código mais recente com o script de limpeza
            "cd /var/app/hc-uti-manager && git pull origin master",
            
            # 2. Atualizar MOCK_BEDS para false (Tarefa 2.1)
            "sed -i 's/MOCK_BEDS=true/MOCK_BEDS=false/g' /var/app/hc-uti-manager/.env",
            
            # 3. Copiar o script para a pasta montada no container (data/)
            "cp /var/app/hc-uti-manager/scratch/production_cleanup.py /var/app/hc-uti-manager/data/production_cleanup.py",
            
            # 4. Executar o script de limpeza dentro do container backend (Tarefa 2.2)
            "podman exec -i hc-uti-backend python /app/data/production_cleanup.py",
            
            # 5. Remover o script temporário do volume
            "rm -f /var/app/hc-uti-manager/data/production_cleanup.py",
            
            # 6. Reiniciar o serviço systemd para validar tudo (Tarefa 2.3)
            "systemctl restart hc-uti.service",
            "sleep 8"
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
