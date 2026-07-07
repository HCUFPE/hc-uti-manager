import os
import paramiko
import sys
from dotenv import load_dotenv

def deploy():
    load_dotenv()
    host = os.getenv("VM_HOST")
    user = os.getenv("VM_USER")
    secret = os.getenv("VM_PASSWORD")

    if not all([host, user, secret]):
        print("Error: VM connection variables (VM_HOST, VM_USER, VM_PASSWORD) are not fully configured in .env")
        sys.exit(1)

    print(f"Connecting to VM {host}...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(hostname=host, username=user, password=secret, timeout=30)
        print("Connected successfully!")
        
        commands = [
            "cd /var/app/hc-uti-manager && git pull origin master",
            "systemctl restart hc-uti.service",
            "sleep 8",  # Aguarda a inicialização do container
            "podman exec hc-uti-backend alembic upgrade head"
        ]
        
        for cmd in commands:
            print(f"Executing command: {cmd}")
            stdin, stdout, stderr = ssh.exec_command(cmd)
            
            # Read outputs
            out = stdout.read().decode('utf-8', errors='ignore')
            err = stderr.read().decode('utf-8', errors='ignore')
            
            if out:
                print("STDOUT:")
                print(out)
            if err:
                print("STDERR:")
                print(err)
                
            status = stdout.channel.recv_exit_status()
            print(f"Command exit status: {status}")
            if status != 0:
                print("Error executing command. Aborting.")
                sys.exit(1)
                
        print("Deployment finished successfully!")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
    finally:
        ssh.close()

if __name__ == "__main__":
    deploy()
