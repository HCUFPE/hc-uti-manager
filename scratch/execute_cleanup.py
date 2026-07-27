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
        
        # 0. Puxar as últimas alterações na VM
        cmd_pull = "cd /var/app/hc-uti-manager && git pull origin master"
        print(f"Executing: {cmd_pull}")
        stdin, stdout, stderr = ssh.exec_command(cmd_pull)
        print("STDOUT:", stdout.read().decode('utf-8', errors='ignore'))

        # 1. Copiar o script para dentro do container
        cmd_cp = "podman cp /var/app/hc-uti-manager/scratch/cleanup_all_duplicates.py hc-uti-backend:/app/cleanup_all_duplicates.py"
        print(f"Executing: {cmd_cp}")
        stdin, stdout, stderr = ssh.exec_command(cmd_cp)
        print("STDERR (copy):", stderr.read().decode('utf-8', errors='ignore'))
        
        # 2. Executar o script no container
        cmd_run = "podman exec hc-uti-backend python /app/cleanup_all_duplicates.py"
        print(f"Executing: {cmd_run}")
        stdin, stdout, stderr = ssh.exec_command(cmd_run)
        print("STDOUT:", stdout.read().decode('utf-8', errors='ignore'))
        print("STDERR:", stderr.read().decode('utf-8', errors='ignore'))
        
    except Exception as e:
        print("Error:", e)
    finally:
        ssh.close()

if __name__ == '__main__':
    main()
