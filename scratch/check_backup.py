import os
import paramiko
from dotenv import load_dotenv

def main():
    load_dotenv()
    host = os.getenv("VM_HOST")
    user = os.getenv("VM_USER")
    secret = os.getenv("VM_PASSWORD")

    print(f"Conectando à VM de Produção {host}...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=secret, timeout=15)
        
        commands = [
            "echo '=== DIFF DE MODIFICAÇÕES NO SCRIPT DE BACKUP ==='",
            "cd /var/app/hc-uti-manager && git diff scratch/backup_db.sh",
            "echo '=== ARQUIVOS DE BACKUP GERADOS ==='",
            "ls -lh /var/app/hc-uti-manager/data/backups/",
            "echo '=== AGENDAMENTO CRON (CRONTAB) ==='",
            "crontab -l",
            "echo '=== LOGS CRON RECENTES ==='",
            "grep -i backup /var/log/cron | tail -n 10 || journalctl -u cron | grep backup | tail -n 10"
        ]
        
        for cmd in commands:
            print(f"\n$ {cmd}")
            stdin, stdout, stderr = ssh.exec_command(cmd)
            # Safe print avoiding unicode bullets
            out = stdout.read().decode('utf-8', errors='ignore')
            print(out)
            err = stderr.read().decode('utf-8', errors='ignore')
            if err:
                print("STDERR:", err)
                
    except Exception as e:
        print("Erro ao executar script:", e)
    finally:
        ssh.close()

if __name__ == '__main__':
    main()
