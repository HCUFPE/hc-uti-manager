import os
import paramiko
from dotenv import load_dotenv

def main():
    load_dotenv()
    host = os.getenv("VM_HOST")
    user = os.getenv("VM_USER")
    secret = os.getenv("VM_PASSWORD")

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(host, username=user, password=secret, timeout=15)
        print("Connected. Running df -h:")
        stdin, stdout, stderr = ssh.exec_command("df -h")
        print(stdout.read().decode('utf-8'))

        print("Pruning podman builds and images:")
        stdin, stdout, stderr = ssh.exec_command("podman system prune -af && podman image prune -af")
        print(stdout.read().decode('utf-8'))
        print(stderr.read().decode('utf-8'))

        print("Running clean on package manager caches if applicable:")
        stdin, stdout, stderr = ssh.exec_command("apt-get clean || yum clean all")
        
        print("Running df -h again:")
        stdin, stdout, stderr = ssh.exec_command("df -h")
        print(stdout.read().decode('utf-8'))
    except Exception as e:
        print("Error:", e)
    finally:
        ssh.close()

if __name__ == '__main__':
    main()
