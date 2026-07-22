import os
import paramiko
from dotenv import load_dotenv

def check_vm_paths():
    load_dotenv()
    host = os.getenv("VM_HOST")
    user = os.getenv("VM_USER")
    secret = os.getenv("VM_PASSWORD")

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(host, username=user, password=secret, timeout=15)
        
        # List files in application folders and show systemd units status
        cmd = """
        echo "=== /var/app/ Contents ==="
        ls -la /var/app/
        
        echo "=== UTI Database Info ==="
        ls -lh /var/app/hc-uti-manager/data/app.db || echo "No UTI DB found"
        
        echo "=== Anatomia Patologica Folder Contents ==="
        ls -la /var/app/hc-anatomia-patologica || echo "No AP folder found"
        
        echo "=== Systemd Services status ==="
        systemctl status hc-uti.service --no-pager || echo "UTI service error"
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
    out, err = check_vm_paths()
    if out:
        print("STDOUT:\n", out.encode('ascii', errors='replace').decode('ascii'))
    if err:
        print("STDERR:\n", err.encode('ascii', errors='replace').decode('ascii'))
