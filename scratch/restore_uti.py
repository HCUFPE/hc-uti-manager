import os
import paramiko
from dotenv import load_dotenv

def restore_uti_system():
    load_dotenv()
    host = os.getenv("VM_HOST")
    user = os.getenv("VM_USER")
    secret = os.getenv("VM_PASSWORD")

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(host, username=user, password=secret, timeout=15)
        
        # 1. Stop the other service/containers if running
        # 2. Restart the UTI service
        cmd = """
        echo "=== Stopping Anatomia Patologica ==="
        cd /var/app/hc-anatomia-patologica && podman-compose down || echo "Already down"
        
        echo "=== Starting UTI Service ==="
        systemctl start hc-uti.service
        
        echo "=== Checking Service Status ==="
        systemctl status hc-uti.service --no-pager
        
        echo "=== Checking Running Containers ==="
        podman ps
        """
        stdin, stdout, stderr = ssh.exec_command(cmd)
        out = stdout.read().decode('utf-8', errors='ignore')
        err = stderr.read().decode('utf-8', errors='ignore')
        return out, err
    except Exception as e:
        print("Error:", e)
        return None, None
    finally:
        ssh.close()

if __name__ == "__main__":
    out, err = restore_uti_system()
    if out:
        print("STDOUT:\n", out.encode('ascii', errors='replace').decode('ascii'))
    if err:
        print("STDERR:\n", err.encode('ascii', errors='replace').decode('ascii'))
