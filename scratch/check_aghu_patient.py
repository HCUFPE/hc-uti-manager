import os
import paramiko
import json
from dotenv import load_dotenv

def run_aghu_query(query, params=None):
    load_dotenv()
    host = os.getenv("VM_HOST")
    user = os.getenv("VM_USER")
    secret = os.getenv("VM_PASSWORD")

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(host, username=user, password=secret, timeout=15)
        
        py_code = """
import os
import json
import asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

async def main():
    dsn = "postgresql+asyncpg://ugen_integra:aghuintegracao@10.34.0.92:6544/dbaghu"
    engine = create_async_engine(dsn)
    async with engine.connect() as conn:
        q1 = "SELECT i.seq, i.lto_lto_id, i.ind_saida_pac, i.dthr_internacao, i.criado_em, p.prontuario, p.nome FROM agh.ain_internacoes i JOIN agh.aip_pacientes p ON i.pac_codigo = p.codigo WHERE p.prontuario = 16309536"
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

if __name__ == '__main__':
    res = run_aghu_query("")
    print(res)
