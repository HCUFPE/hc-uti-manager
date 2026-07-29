import os
import paramiko
from dotenv import load_dotenv

def main():
    load_dotenv(r"c:\Users\daniel.turmina\Documents\HC-uti-manager\.env")
    host = os.getenv("VM_HOST")
    user = os.getenv("VM_USER")
    secret = os.getenv("VM_PASSWORD")

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(host, username=user, password=secret, timeout=15)
        
        # Buscar TODOS os eventos de histórico de hoje relacionados a trocas ou substituições
        query = "select id, tipo, acao, criado_em, detalhes from historico_acoes where criado_em >= '2026-07-29 00:00:00' and (detalhes like '%troca%' or detalhes like '%substitu%' or detalhes like '%21036074%' or detalhes like '%22307987%' or detalhes like '%13938907%');"
        cmd = f"export XDG_RUNTIME_DIR=/run/user/$(id -u) && podman exec hc-uti-backend python -c \"import sqlite3; conn = sqlite3.connect('/app/data/app.db'); [print(row) for row in conn.execute('{query}').fetchall()]; conn.close()\""
        
        stdin, stdout, stderr = ssh.exec_command(cmd)
        print("All Swap/Substitutions History for Today:")
        print(stdout.read().decode('utf-8'))
            
    except Exception as e:
        print("Error:", e)
    finally:
        ssh.close()

if __name__ == '__main__':
    main()
