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
        
        cmd = 'podman exec hc-uti-backend python -c "import sqlite3; c=sqlite3.connect(\'/app/data/app.db\'); print(c.execute(\'SELECT data, taxa_ocupacao FROM historico_ocupacao ORDER BY data DESC LIMIT 7\').fetchall())"'
        stdin, stdout, stderr = ssh.exec_command(cmd)
        
        print("=== HISTÓRICO DE OCUPAÇÃO GRAVADO ===")
        print(stdout.read().decode('utf-8'))
        
        cmd2 = 'ls -lh /var/app/hc-uti-manager/data/backups'
        stdin2, stdout2, stderr2 = ssh.exec_command(cmd2)
        print("=== ARQUIVOS DE BACKUP GERADOS ===")
        print(stdout2.read().decode('utf-8'))

    except Exception as e:
        print("Erro:", e)
    finally:
        ssh.close()

if __name__ == '__main__':
    main()
