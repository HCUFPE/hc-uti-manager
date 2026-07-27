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
        
        # Python script to run inside the container to find and delete duplicates
        py_cmd = (
            "import sqlite3; "
            "conn = sqlite3.connect('/app/data/app.db'); "
            "cursor = conn.cursor(); "
            # 1. Encontrar todos os alertas
            "cursor.execute('SELECT id, titulo, mensagem, criado_em FROM alertas;'); "
            "rows = cursor.fetchall(); "
            "duplicates = []; "
            "seen = {}; " # chave: (mensagem, criado_em) -> list of ids/rows
            "for r in rows: "
            "    id_val, tit, msg, date = r; "
            "    key = (msg, date); "
            "    seen.setdefault(key, []).append(r); "
            
            # Encontra grupos duplicados (mesma mensagem e mesma data)
            "to_delete = []; "
            "for key, items in seen.items(): "
            "    if len(items) > 1: "
            "        print('Duplicados encontrados:', items); "
            "        # Se houver um de alteracao e um de definicao, preferimos manter o de alteracao e deletar o de definicao, "
            "        # ou simplesmente deletar o excedente se forem idênticos. "
            "        # Mas o usuário pediu especificamente para deletar o ID 196: "
            "        for it in items: "
            "            id_val = it[0]; "
            "            title = it[1]; "
            "            # Se for o ID 196, ou se for o de 'Destino de Alta Definido' do par duplicado: "
            "            if id_val == 196: "
            "                to_delete.append(id_val); "
            "            elif len(items) == 2 and title == \"Destino de Alta Definido\" and id_val != 196: "
            "                # Se mantivermos o 196, deletamos o outro "
            "                pass; "
            
            # Caso o usuário queira limpar os de ID 196 especificamente, adicionamos aqui:
            "if 196 not in to_delete: "
            "    to_delete.append(196); " # Forçar exclusão do 196
            
            "print('IDs marcados para delecao:', to_delete); "
            "for d_id in to_delete: "
            "    cursor.execute('DELETE FROM alertas WHERE id = ?;', (d_id,)); "
            "conn.commit(); "
            "print('Delecao realizada com sucesso!'); "
            "conn.close(); "
        )
        
        cmd = f"podman exec hc-uti-backend python -c \"{py_cmd}\""
        print(f"Executing: {cmd}")
        stdin, stdout, stderr = ssh.exec_command(cmd)
        print("STDOUT:")
        print(stdout.read().decode('utf-8', errors='ignore'))
        print("STDERR:")
        print(stderr.read().decode('utf-8', errors='ignore'))
        
    except Exception as e:
        print("Error:", e)
    finally:
        ssh.close()

if __name__ == '__main__':
    main()
