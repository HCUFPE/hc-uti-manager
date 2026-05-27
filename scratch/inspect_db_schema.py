import paramiko
import sys

def inspect_db():
    host = "10.34.0.192"
    user = "root"
    password = "hc*l0ck2025"
    db_path = "/var/app/hc-uti-manager/data/app.db"
    
    print(f"Connecting to {host} as {user}...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=password, timeout=10)
        print("Connected successfully!")
    except Exception as e:
        print(f"Failed to connect: {e}")
        sys.exit(1)
        
    # Execute sqlite3 check inside the VM
    cmd = f'python3 -c "import sqlite3; conn = sqlite3.connect(\'{db_path}\'); cur = conn.cursor(); cur.execute(\'PRAGMA table_info(solicitacoes_leito)\'); cols = [row[1] for row in cur.fetchall()]; print(\'Columns in solicitacoes_leito:\', cols); conn.close()"'
    
    stdin, stdout, stderr = ssh.exec_command(cmd)
    
    print("STDOUT:")
    print(stdout.read().decode('utf-8'))
    print("STDERR:")
    print(stderr.read().decode('utf-8'))
    
    ssh.close()

if __name__ == "__main__":
    inspect_db()
