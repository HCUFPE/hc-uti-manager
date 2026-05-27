import paramiko
import sys

def view_env():
    host = "10.34.0.192"
    user = "root"
    password = "hc*l0ck2025"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=password, timeout=10)
    except Exception as e:
        print(f"Failed to connect: {e}")
        sys.exit(1)
        
    stdin, stdout, stderr = ssh.exec_command("cat /var/app/hc-uti-manager/.env")
    print("VM .env File Content:")
    print(stdout.read().decode('utf-8'))
    
    ssh.close()

if __name__ == "__main__":
    view_env()
