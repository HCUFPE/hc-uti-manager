import os
import paramiko
from dotenv import load_dotenv

def cleanup_anatomia():
    load_dotenv()
    host = os.getenv("VM_HOST")
    user = os.getenv("VM_USER")
    secret = os.getenv("VM_PASSWORD")

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(host, username=user, password=secret, timeout=15)
        
        # 1. Stop and remove any remaining anatomia containers or networks
        # 2. Delete the anatomia patologica directory completely
        cmd = """
        echo "=== Stopping any AP containers ==="
        if [ -d "/var/app/hc-anatomia-patologica" ]; then
            cd /var/app/hc-anatomia-patologica
            podman-compose down || true
            cd /var/app
            echo "=== Deleting /var/app/hc-anatomia-patologica ==="
            rm -rf /var/app/hc-anatomia-patologica
        else
            echo "Anatomia folder already removed."
        fi
        
        echo "=== Pruning unused podman networks and images ==="
        podman network prune -f || true
        podman image prune -a -f || true
        
        echo "=== /var/app/ Current Contents ==="
        ls -la /var/app/
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
    out, err = cleanup_anatomia()
    if out:
        print("STDOUT:\n", out.encode('ascii', errors='replace').decode('ascii'))
    if err:
        print("STDERR:\n", err.encode('ascii', errors='replace').decode('ascii'))
