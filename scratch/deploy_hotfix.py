import os
import paramiko
from dotenv import load_dotenv

def main():
    load_dotenv()
    host = os.getenv("VM_HOST")
    user = os.getenv("VM_USER")
    secret = os.getenv("VM_PASSWORD")

    print(f"Conectando a {host} como {user}...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=secret, timeout=15)
        print("Conectado! Iniciando transferência SFTP...")
        
        sftp = ssh.open_sftp()
        local_file = r"c:\Users\daniel.turmina\Documents\HC-uti-manager\frontend\src\views\Home.vue"
        remote_file = "/var/app/hc-uti-manager/frontend/src/views/Home.vue"
        
        sftp.put(local_file, remote_file)
        sftp.close()
        print(f"Arquivo {local_file} enviado com sucesso para {remote_file} na VM!")
        
        print("Reiniciando o serviço hc-uti para rebuildar e subir o frontend atualizado...")
        stdin, stdout, stderr = ssh.exec_command("systemctl restart hc-uti")
        
        err = stderr.read().decode('utf-8')
        if err:
            print("Erro ao reiniciar serviço:", err)
        else:
            print("Serviço hc-uti reiniciado com sucesso! O rebuild do podman-compose foi disparado.")
            
    except Exception as e:
        print("Erro durante o deploy:", e)
    finally:
        ssh.close()

if __name__ == '__main__':
    main()
