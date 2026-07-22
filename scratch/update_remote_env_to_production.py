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
        
        commands = [
            # 1. Update ENV to production in .env
            "sed -i 's/ENV=development/ENV=production/g' /var/app/hc-uti-manager/.env",
            
            # 2. Restart the systemd service to apply the change
            "systemctl restart hc-uti.service",
            "sleep 3",
            
            # 3. Check status
            "systemctl status hc-uti.service"
        ]
        
        for cmd in commands:
            print(f"Executing: {cmd}")
            stdin, stdout, stderr = ssh.exec_command(cmd)
            print("STDOUT:")
            print(stdout.read().decode('utf-8', errors='ignore'))
            print("STDERR:")
            print(stderr.read().decode('utf-8', errors='ignore'))
            
    except Exception as e:
        print("Error:", e)
    finally:
        ssh.close()

if __name__ == '__main__':
    main()
