import os
import paramiko
import json
from dotenv import load_dotenv

def run_container_python_query(query, params=None):
    load_dotenv()
    host = os.getenv("VM_HOST")
    user = os.getenv("VM_USER")
    secret = os.getenv("VM_PASSWORD")

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(host, username=user, password=secret, timeout=15)
        
        py_code = f"""
import sqlite3
import json

conn = sqlite3.connect('/app/data/app.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()
try:
    cursor.execute({repr(query)}, {repr(params or [])})
    rows = [dict(r) for r in cursor.fetchall()]
    print(json.dumps(rows, default=str))
except Exception as e:
    print(json.dumps({{"error": str(e)}}))
finally:
    conn.close()
"""
        cmd = "podman exec -i hc-uti-backend python"
        stdin, stdout, stderr = ssh.exec_command(cmd)
        stdin.write(py_code)
        stdin.flush()
        stdin.channel.shutdown_write()
        
        out = stdout.read().decode('utf-8', errors='ignore')
        return out
    except Exception as e:
        print("Error:", e)
        return None
    finally:
        ssh.close()

def run_aghu_query():
    load_dotenv()
    host = os.getenv("VM_HOST")
    user = os.getenv("VM_USER")
    secret = os.getenv("VM_PASSWORD")

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(host, username=user, password=secret, timeout=15)
        py_code = """
import json
import asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

async def main():
    dsn = "postgresql+asyncpg://ugen_integra:aghuintegracao@10.34.0.92:6544/dbaghu"
    engine = create_async_engine(dsn)
    async with engine.connect() as conn:
        q1 = "SELECT i.seq, i.lto_lto_id, i.ind_saida_pac, p.prontuario, p.nome FROM agh.ain_internacoes i JOIN agh.aip_pacientes p ON i.pac_codigo = p.codigo WHERE p.prontuario = 21277611"
        res1 = await conn.execute(text(q1))
        rows1 = [dict(r) for r in res1.mappings().all()]
        print(json.dumps({"internacoes": rows1}, default=str))
    await engine.dispose()

asyncio.run(main())
"""
        cmd = "podman exec -i hc-uti-backend python"
        stdin, stdout, stderr = ssh.exec_command(cmd)
        stdin.write(py_code)
        stdin.flush()
        stdin.channel.shutdown_write()
        out = stdout.read().decode('utf-8', errors='ignore')
        return out
    except Exception as e:
        print("Error:", e)
        return None
    finally:
        ssh.close()

def main():
    print("--- SOLICITACOES LEITO (21277611) ---")
    res_sol = run_container_python_query("SELECT * FROM solicitacoes_leito WHERE prontuario = ?", ["21277611"])
    try:
        data = json.loads(res_sol)
        print(json.dumps(data, indent=2, ensure_ascii=False))
    except:
        print(res_sol)

    print("\n--- AGHU INTERNACOES (21277611) ---")
    res_aghu = run_aghu_query()
    try:
        data = json.loads(res_aghu)
        print(json.dumps(data, indent=2, ensure_ascii=False))
    except:
        print(res_aghu)

if __name__ == '__main__':
    main()
