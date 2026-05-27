import paramiko
import sys

def inspect_logs():
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
        
    commands = [
        ("Nginx Container Logs", "podman logs hc-uti-nginx"),
        ("Backend Container Logs", "podman logs hc-uti-backend"),
        ("Check active containers", "podman ps"),
        ("Check systemctl service status", "systemctl status hc-uti.service --no-pager")
    ]
    
    for desc, cmd in commands:
        print("\n" + "="*50)
        print(f"Running: {desc}")
        print(f"Command: {cmd}")
        print("="*50)
        
        stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
        exit_status = stdout.channel.recv_exit_status()
        
        out_lines = stdout.read().decode('utf-8', errors='replace')
        err_lines = stderr.read().decode('utf-8', errors='replace')
        
        out_clean = out_lines.encode('ascii', errors='replace').decode('ascii')
        err_clean = err_lines.encode('ascii', errors='replace').decode('ascii')
        
        if out_clean:
            print("[STDOUT]")
            print(out_clean.strip())
        if err_clean:
            print("[STDERR]")
            print(err_clean.strip())
            
        print(f"Exit Code: {exit_status}")
        
    ssh.close()

if __name__ == "__main__":
    inspect_logs()
