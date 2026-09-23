import os
import paramiko
from dotenv import load_dotenv

def main():
    load_dotenv()
    host = os.getenv("VM_HOST_HOMOLOGACAO")
    user = os.getenv("VM_USER_HOMOLOGACAO")
    secret = os.getenv("VM_PASSWORD_HOMOLOGACAO")

    if not host or not user or not secret:
        print("Erro: As variáveis de ambiente VM_HOST_HOMOLOGACAO, VM_USER_HOMOLOGACAO e VM_PASSWORD_HOMOLOGACAO devem estar configuradas no arquivo .env")
        return

    print(f"Conectando à VM de Homologação ({host}) como '{user}'...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(host, username=user, password=secret, timeout=15)
        print("Conexão SSH estabelecida com sucesso!")
        
        # 1. Enviar arquivos locais atualizados para a VM de homologação via SFTP
        sftp = ssh.open_sftp()
        local_root = r"c:\Users\daniel.turmina\Documents\HC-uti-manager"
        
        def upload_dir(local, remote):
            try: sftp.mkdir(remote)
            except: pass
            for item in os.listdir(local):
                l_path = os.path.join(local, item)
                r_path = f"{remote}/{item}"
                if os.path.isdir(l_path):
                    if item not in [".git", "node_modules", ".venv", "__pycache__", ".agents", "scratch"]:
                        upload_dir(l_path, r_path)
                else:
                    if not item.endswith('.pyc') and not item.startswith('.'):
                        sftp.put(l_path, r_path)

        upload_dir(os.path.join(local_root, "src"), "/var/app/hc-uti-manager/src")
        upload_dir(os.path.join(local_root, "frontend"), "/var/app/hc-uti-manager/frontend")
        sftp.close()

        # Sequência de comandos de deploy na VM de homologação
        commands = [
            # 2. Reiniciar containers via podman-compose re-building imagens
            "cd /var/app/hc-uti-manager && podman-compose down 2>/dev/null || true",
            "cd /var/app/hc-uti-manager && podman-compose up -d --build",
            
            # 3. Aguarda a inicialização completa do container
            "until [ \"$(podman inspect -f '{{.State.Running}}' hc-uti-backend-homolog 2>/dev/null || podman inspect -f '{{.State.Running}}' hc-uti-backend 2>/dev/null)\" = \"true\" ]; do echo 'Aguardando inicializacao do container...'; sleep 3; done",
            
            # 4. Executar migrações do Alembic se houver
            "podman exec -i hc-uti-backend-homolog alembic upgrade head 2>&1 || podman exec -i hc-uti-backend alembic upgrade head 2>&1 || true"
        ]
        
        for cmd in commands:
            print(f"\nExecutando: {cmd}")
            stdin, stdout, stderr = ssh.exec_command(cmd)
            out_str = stdout.read().decode('utf-8', errors='ignore')
            err_str = stderr.read().decode('utf-8', errors='ignore')
            
            safe_out = out_str.encode('ascii', errors='replace').decode('ascii')
            safe_err = err_str.encode('ascii', errors='replace').decode('ascii')
            
            if safe_out:
                print("STDOUT:")
                print(safe_out)
            if safe_err:
                print("STDERR:")
                print(safe_err)
                
        print("\nDeploy em Homologação concluído com sucesso!")
            
    except Exception as e:
        print("Erro durante o deploy:", e)
    finally:
        ssh.close()

if __name__ == '__main__':
    main()
