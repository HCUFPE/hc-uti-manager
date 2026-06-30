import os
import paramiko
import sys
from dotenv import load_dotenv

def run_cmd(ssh, cmd):
    print(f"\n--- Executing: {cmd} ---")
    stdin, stdout, stderr = ssh.exec_command(cmd)
    
    # Read output
    out = stdout.read().decode('utf-8', errors='ignore')
    if out:
        print(out)
    err = stderr.read().decode('utf-8', errors='ignore')
    if err:
        print("STDERR:", err)
        
    status = stdout.channel.recv_exit_status()
    print(f"Exit status: {status}")
    return status == 0

def main():
    load_dotenv()
    vm_host = os.getenv("VM_HOST")
    vm_user = os.getenv("VM_USER")
    vm_password = os.getenv("VM_PASSWORD")
    
    if not all([vm_host, vm_user, vm_password]):
        print("Error: VM connection variables (VM_HOST, VM_USER, VM_PASSWORD) are not fully configured in .env")
        sys.exit(1)

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(f"Connecting to {vm_host}...")
        ssh.connect(vm_host, username=vm_user, password=vm_password)
        print("Connected successfully!")
        
        # 1. Limpar os dados do banco SQLite na VM
        # O banco SQLite normalmente está em /var/app/hc-uti-manager/data/app.db
        # Vamos rodar um comando sqlite3 diretamente no arquivo se sqlite3 estiver instalado,
        # ou rodar um script python na VM que faça isso, ou simplesmente apagar e recriar/rodar migrations?
        # A forma mais segura é rodar comandos SQL usando sqlite3 ou python. Vamos tentar rodar via python na VM.
        python_clean_cmd = (
            "python3 -c \""
            "import sqlite3; "
            "conn = sqlite3.connect('/var/app/hc-uti-manager/data/app.db'); "
            "cursor = conn.cursor(); "
            "[cursor.execute(f'DELETE FROM {t}') for t in ['solicitacoes_leito', 'solicitacoes_alta', 'historico_acoes', 'alertas', 'refresh_tokens', 'leito_estados']]; "
            "conn.commit(); "
            "conn.close(); "
            "print('VM Database cleaned successfully!');\""
        )
        print("Cleaning VM Database...")
        run_cmd(ssh, python_clean_cmd)

        # 2. Update repo on VM (para atualizar com o mock do paciente 8)
        print("Updating repository on VM with new mock rule...")
        run_cmd(ssh, "cd /var/app/hc-uti-manager && git fetch origin && git reset --hard origin/master")
        
        # 3. Restart systemd service
        print("Restarting systemd hc-uti service...")
        run_cmd(ssh, "systemctl restart hc-uti.service")
        
    except Exception as e:
        print("Error:", e)
    finally:
        ssh.close()

if __name__ == '__main__':
    main()
