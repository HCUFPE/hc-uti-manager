import os
import paramiko
from dotenv import load_dotenv

def recursive_upload(sftp, local_dir, remote_dir, excludes=None):
    if excludes is None:
        excludes = []
        
    base = os.path.basename(local_dir)
    if base in excludes or base.startswith('.'):
        return
        
    try:
        sftp.mkdir(remote_dir)
    except IOError:
        pass

    for item in os.listdir(local_dir):
        local_path = os.path.join(local_dir, item)
        remote_path = f"{remote_dir}/{item}"
        
        if os.path.isdir(local_path):
            recursive_upload(sftp, local_path, remote_path, excludes)
        else:
            filename = os.path.basename(local_path)
            if filename in excludes or filename.endswith('.pyc') or filename.startswith('.'):
                continue
            sftp.put(local_path, remote_path)

def main():
    load_dotenv()
    host = os.getenv("VM_HOST_HOMOLOGACAO")
    user = os.getenv("VM_USER_HOMOLOGACAO")
    secret = os.getenv("VM_PASSWORD_HOMOLOGACAO")

    print(f"Conectando a VM de homologacao {host} como {user}...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=secret, timeout=15)
        print("Conectado! Iniciando Deploy de Homologacao...")
        
        # Parar antigo pija se existir
        ssh.exec_command("cd /var/app/pija && podman-compose down")
        ssh.exec_command("podman stop pija_nginx_1 pija_pija-backend_1; podman rm pija_nginx_1 pija_pija-backend_1")
        ssh.exec_command("rm -rf /var/app/pija")
        
        # Criar pastas do UTI manager
        ssh.exec_command("mkdir -p /var/app/hc-uti-manager/nginx")
        ssh.exec_command("mkdir -p /var/app/hc-uti-manager/data")
        
        sftp = ssh.open_sftp()
        
        excludes = [
            ".venv", ".git", "node_modules", ".agents", "openspec", 
            "__pycache__", "dist", ".nuxt", "scratch", ".system_generated",
            "click_feedback", "task.md", "walkthrough.md"
        ]
        
        local_root = r"c:\Users\daniel.turmina\Documents\HC-uti-manager"
        
        # Copiar pastas
        recursive_upload(sftp, os.path.join(local_root, "src"), "/var/app/hc-uti-manager/src", excludes)
        recursive_upload(sftp, os.path.join(local_root, "frontend"), "/var/app/hc-uti-manager/frontend", excludes)
        recursive_upload(sftp, os.path.join(local_root, "alembic"), "/var/app/hc-uti-manager/alembic", excludes)
        
        # Copiar arquivos de configuracao
        root_files = [
            ("Dockerfile", "Dockerfile"),
            ("alembic.ini", "alembic.ini"),
            ("requirements.txt", "requirements.txt"),
            ("docker-compose.homolog.yaml", "docker-compose.yaml")
        ]
        for local_name, remote_name in root_files:
            sftp.put(os.path.join(local_root, local_name), f"/var/app/hc-uti-manager/{remote_name}")

        # Upload e customização do .env (MOCK_BEDS=false, MOCK_AUTH=false)
        l_env = os.path.join(local_root, ".env")
        r_env = "/var/app/hc-uti-manager/.env"
        with open(l_env, "r", encoding="utf-8") as f:
            env_content = f.read()
        
        import re
        if "MOCK_BEDS=" in env_content:
            env_content = re.sub(r"MOCK_BEDS=\w+", "MOCK_BEDS=false", env_content)
        else:
            env_content += "\nMOCK_BEDS=false\n"

        if "MOCK_AUTH=" in env_content:
            env_content = re.sub(r"MOCK_AUTH=\w+", "MOCK_AUTH=false", env_content)
        else:
            env_content += "\nMOCK_AUTH=false\n"
            
        with sftp.file(r_env, "w") as remote_file:
            remote_file.write(env_content)
            
        # Nginx Config
        sftp.put(os.path.join(local_root, "nginx", "default.homolog.conf"), "/var/app/hc-uti-manager/nginx/default.conf")
        
        # SQLite DB actual state - apenas envia se não existir na VM para evitar sobrescrever dados de teste
        l_db = os.path.join(local_root, "data", "app.db")
        if os.path.exists(l_db):
            try:
                sftp.stat("/var/app/hc-uti-manager/data/app.db")
                print("Banco de dados ja existe na VM de homologacao. Ignorando upload para preservar dados de teste.")
            except IOError:
                print("Banco de dados nao encontrado na VM. Enviando banco SQLite inicial...")
                sftp.put(l_db, "/var/app/hc-uti-manager/data/app.db")
            
        sftp.close()
        
        print("Arquivos enviados. Iniciando stack na VM de homologacao...")
        stdin, stdout, stderr = ssh.exec_command("cd /var/app/hc-uti-manager && podman-compose down && podman-compose up -d --build")
        stdout.channel.recv_exit_status()
        print("Deploy concluído com sucesso!")
            
    except Exception as e:
        print("Erro durante deploy:", e)
    finally:
        ssh.close()

if __name__ == '__main__':
    main()
