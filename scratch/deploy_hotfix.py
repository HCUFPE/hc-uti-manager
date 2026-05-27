import paramiko
import sys
import time

def deploy_hotfix():
    host = "10.34.0.192"
    user = "root"
    password = "hc*l0ck2025"
    
    print(f"Connecting to {host} as {user}...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=password, timeout=10)
        print("Connected successfully!")
    except Exception as e:
        print(f"Failed to connect: {e}")
        sys.exit(1)
        
    def run_safe_cmd(cmd):
        stdin, stdout, stderr = ssh.exec_command(cmd)
        out = stdout.read().decode('utf-8', errors='replace')
        err = stderr.read().decode('utf-8', errors='replace')
        out_clean = out.encode('ascii', errors='replace').decode('ascii')
        err_clean = err.encode('ascii', errors='replace').decode('ascii')
        return out_clean, err_clean

    print("\n--- Running git pull on VM ---")
    out, err = run_safe_cmd("cd /var/app/hc-uti-manager && git pull")
    print("Git Pull Output:")
    print(out.strip())
    if err:
        print("Git Pull Error:", err.strip())
        
    print("\n--- Restarting hc-uti.service ---")
    out, err = run_safe_cmd("systemctl restart hc-uti.service")
    if err:
        print("Restart Error:", err.strip())
        
    print("\nWaiting 15 seconds for rebuild and container initialization...")
    time.sleep(15)
    
    print("\n--- systemctl status hc-uti.service ---")
    out, err = run_safe_cmd("systemctl status hc-uti.service --no-pager")
    print(out)
    
    print("\n--- podman ps -a ---")
    out, err = run_safe_cmd("podman ps -a")
    print(out)
    
    print("\n--- Backend logs (last 30 lines) ---")
    out, err = run_safe_cmd("podman logs --tail 30 hc-uti-backend")
    print(out.strip())
    if err:
        print("Backend Logs Error:", err.strip())
        
    ssh.close()

if __name__ == "__main__":
    deploy_hotfix()
