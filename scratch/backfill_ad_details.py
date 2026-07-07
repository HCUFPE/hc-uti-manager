import os
import paramiko
import sys
from dotenv import load_dotenv

def main():
    load_dotenv()
    host = os.getenv("VM_HOST")
    user = os.getenv("VM_USER")
    secret = os.getenv("VM_PASSWORD")

    if not all([host, user, secret]):
        print("Error: VM connection variables (VM_HOST, VM_USER, VM_PASSWORD) are not fully configured in .env")
        sys.exit(1)

    # Python script that will be executed inside the container
    container_script = """
import os
import sys
import sqlite3
from dotenv import load_dotenv
from ldap3 import Server, Connection, ALL, SUBTREE, ALL_ATTRIBUTES

load_dotenv('.env')
ad_url = os.getenv('AD_URL')
ad_basedn = os.getenv('AD_BASEDN')
bind_user = os.getenv('AD_BIND_USER')
bind_pass = os.getenv('AD_BIND_PASSWORD')

if not all([ad_url, ad_basedn, bind_user, bind_pass]):
    print('Error: AD configuration missing or incomplete in container .env')
    sys.exit(1)

# Connect to SQLite
db_path = 'data/app.db'
if not os.path.exists(db_path):
    print(f'Error: SQLite database not found at {db_path}')
    sys.exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get users
cursor.execute("SELECT id, username FROM usuarios_perfis")
rows = cursor.fetchall()
if not rows:
    print("No custom profiles found in the database. Nothing to backfill.")
    conn.close()
    sys.exit(0)

# Connect to AD
server = Server(ad_url, get_info=ALL)
ldap_conn = Connection(server, user=bind_user, password=bind_pass, receive_timeout=10)
if not ldap_conn.bind():
    print("Error: Failed to bind to LDAP AD")
    conn.close()
    sys.exit(1)

print(f"Found {len(rows)} registered profiles. Querying AD details...")
updated_count = 0
for db_id, username in rows:
    clean_user = username.strip().lower()
    print(f"Processing user: {clean_user}...")
    
    search_filter = f"(&(objectClass=user)(sAMAccountName={clean_user}))"
    ldap_conn.search(search_base=ad_basedn, search_filter=search_filter, search_scope=SUBTREE, attributes=ALL_ATTRIBUTES, size_limit=1)
    
    if not ldap_conn.entries:
        print(f"Warning: User '{clean_user}' not found in AD directory.")
        continue
        
    entry = ldap_conn.entries[0]
    attrs = entry.entry_attributes_as_dict
    
    # Extract attributes
    display_name = attrs.get("displayName", [""])
    if isinstance(display_name, list) and display_name:
        display_name = display_name[0]
    elif not display_name:
        display_name = attrs.get("cn", [""])[0] if attrs.get("cn") else clean_user
        
    department = attrs.get("department", [""])
    if isinstance(department, list) and department:
        department = department[0]
        
    mail = attrs.get("mail", [""])
    if isinstance(mail, list) and mail:
        mail = mail[0]
    elif not mail:
        upn = attrs.get("userPrincipalName", [""])
        if isinstance(upn, list) and upn:
            mail = upn[0]
        else:
            mail = f"{clean_user}@mock.com"
            
    print(f" -> AD Data found: '{display_name}' | '{department}' | '{mail}'")
    cursor.execute(
        "UPDATE usuarios_perfis SET nome_completo = ?, lotacao = ?, email = ? WHERE id = ?",
        (display_name, department, mail, db_id)
    )
    updated_count += 1

conn.commit()
conn.close()
print(f"Backfill finished. Updated {updated_count} user profiles with AD attributes.")
"""

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(f"Connecting to VM {host}...")
        ssh.connect(host, username=user, password=secret, timeout=15)
        
        print("Executing AD backfill script inside 'hc-uti-backend' container...")
        stdin, stdout, stderr = ssh.exec_command("podman exec -i hc-uti-backend python3")
        
        # Pipe script to stdin
        stdin.write(container_script)
        stdin.channel.shutdown_write()
        
        # Read output
        out = stdout.read().decode('utf-8', errors='ignore')
        err = stderr.read().decode('utf-8', errors='ignore')
        
        if out:
            print("STDOUT:")
            print(out.encode('ascii', errors='replace').decode('ascii'))
        if err:
            print("STDERR:")
            print(err.encode('ascii', errors='replace').decode('ascii'))
            
    except Exception as e:
        print("Error:", e)
    finally:
        ssh.close()

if __name__ == '__main__':
    main()
