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
        
        # 1. Verificar tamanho do banco de dados SQLite
        cmd_size = "ls -lh /var/app/hc-uti-manager/data/app.db"
        print(f"Executing: {cmd_size}")
        stdin, stdout, stderr = ssh.exec_command(cmd_size)
        print("STDOUT:", stdout.read().decode('utf-8', errors='ignore'))
        print("STDERR:", stderr.read().decode('utf-8', errors='ignore'))
        
        # 2. Verificar espaço em disco da VM
        cmd_df = "df -h /var/app/hc-uti-manager/data"
        print(f"Executing: {cmd_df}")
        stdin, stdout, stderr = ssh.exec_command(cmd_df)
        print("STDOUT:", stdout.read().decode('utf-8', errors='ignore'))
        
    except Exception as e:
        print("Error:", e)
    finally:
        ssh.close()

if __name__ == '__main__':
    main()
