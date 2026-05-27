import paramiko
import sys

def test_aghu_query():
    host = "10.34.0.192"
    user = "root"
    password = "hc*l0ck2025"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=password, timeout=10)
        print("Connected to VM successfully!")
    except Exception as e:
        print(f"Failed to connect: {e}")
        sys.exit(1)
        
    python_script = """import os
from sqlalchemy import create_engine, text

dsn = os.getenv("POSTGRES_DSN")
# Convert asyncpg DSN to psycopg2 for synchronous inspection if needed
sync_dsn = dsn.replace("asyncpg", "psycopg2") if dsn else None
print("Connecting to:", sync_dsn)

if not sync_dsn:
    print("Error: POSTGRES_DSN not found in env")
    exit(1)

try:
    engine = create_engine(sync_dsn)
    with engine.connect() as conn:
        print("\\n--- Querying recent patient surgeries in AGHU ---")
        sql = '''
        SELECT pac.prontuario, pac.nome, cir.dthr_inicio_cirg, cir.situacao
        FROM agh.mbc_cirurgias cir
        INNER JOIN agh.aip_pacientes pac ON cir.pac_codigo = pac.codigo
        ORDER BY cir.dthr_inicio_cirg DESC
        LIMIT 5
        '''
        res = conn.execute(text(sql))
        rows = res.fetchall()
        print("Recent surgeries:")
        for r in rows:
            print(f"  Prontuario: {r[0]}, Nome: {r[1]}, Data: {r[2]}, Situacao: {r[3]}")
            
        print("\\n--- Checking the full query with one of these prontuarios ---")
        if rows:
            test_pront = rows[0][0]
            print(f"Testing with prontuario: {test_pront}")
            
            # Read query from file inside the container
            query_path = "/app/src/providers/sql/solicitacao/obter_cirurgia_aghu.sql"
            with open(query_path, 'r', encoding='utf-8') as f:
                query_sql = f.read()
                
            res_full = conn.execute(text(query_sql), {"prontuario": str(test_pront)})
            full_row = res_full.fetchone()
            print("Full Query Row:", full_row)
        else:
            print("No surgeries found in mbc_cirurgias!")
            
except Exception as e:
    print("Database inspection error:", e)
"""
    
    # Escape quotes and newlines for bash
    escaped_script = python_script.replace('"', '\\"').replace('$', '\\$')
    cmd = f'podman exec hc-uti-backend python3 -c "{escaped_script}"'
    
    stdin, stdout, stderr = ssh.exec_command(cmd)
    print("Inspection Output:")
    print(stdout.read().decode('utf-8'))
    print("Inspection Error (if any):")
    print(stderr.read().decode('utf-8'))
    
    ssh.close()

if __name__ == "__main__":
    test_aghu_query()
