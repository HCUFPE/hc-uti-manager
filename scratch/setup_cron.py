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
        
        # 1. Dar permissão de execução ao script
        cmd_chmod = "chmod +x /var/app/hc-uti-manager/scratch/backup_db.sh"
        print(f"Executing: {cmd_chmod}")
        ssh.exec_command(cmd_chmod)
        
        # 2. Configurar o Cron Job
        cmd_cron = '(crontab -l 2>/dev/null | grep -v "/var/app/hc-uti-manager/scratch/backup_db.sh"; echo "0 2 * * * /var/app/hc-uti-manager/scratch/backup_db.sh > /dev/null 2>&1") | crontab -'
        print(f"Executing cron registration...")
        stdin, stdout, stderr = ssh.exec_command(cmd_cron)
        print("STDOUT:", stdout.read().decode('utf-8', errors='ignore'))
        print("STDERR:", stderr.read().decode('utf-8', errors='ignore'))
        
        # 3. Verificar se o cron job foi registrado
        cmd_list = "crontab -l"
        print(f"Verifying registered crontab ({cmd_list}):")
        stdin, stdout, stderr = ssh.exec_command(cmd_list)
        print(stdout.read().decode('utf-8', errors='ignore'))
        
    except Exception as e:
        print("Error:", e)
    finally:
        ssh.close()

if __name__ == '__main__':
    main()
