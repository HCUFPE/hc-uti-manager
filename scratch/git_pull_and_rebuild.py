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
            "cd /var/app/hc-uti-manager && git pull origin master",
            "cd /var/app/hc-uti-manager && podman build --no-cache -t localhost/hc-uti-manager_backend:latest .",
            "systemctl restart hc-uti.service",
            "sleep 15",
            "podman exec hc-uti-backend alembic upgrade head"
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
