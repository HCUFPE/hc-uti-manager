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
        
        commands = {
            "Containers (Podman PS)": "podman ps -a",
            "Disk Space (df -h)": "df -h / /var /var/lib/containers",
            "RAM Memory (free -h)": "free -h",
            "Database File Size": "ls -lh /var/app/hc-uti-manager/data/app.db",
            "Podman Stats": "podman stats --no-stream --format 'table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}'"
        }
        
        for title, cmd in commands.items():
            print(f"=== {title} ===")
            stdin, stdout, stderr = ssh.exec_command(cmd)
            out_str = stdout.read().decode('utf-8', errors='ignore')
            print(out_str)
            print()
            
    except Exception as e:
        print("Error:", e)
    finally:
        ssh.close()

if __name__ == '__main__':
    main()
