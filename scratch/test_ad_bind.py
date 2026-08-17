import os
import ldap3
from dotenv import load_dotenv

load_dotenv()
ad_url = os.getenv("AD_URL")
ad_user = os.getenv("AD_BIND_USER")
ad_pass = os.getenv("AD_BIND_PASSWORD")

print(f"Tentando bind no AD:")
print(f"URL: {ad_url}")
print(f"User: {ad_user}")

try:
    server = ldap3.Server(ad_url, get_info=ldap3.ALL)
    conn = ldap3.Connection(server, user=ad_user, password=ad_pass, receive_timeout=10)
    result = conn.bind()
    print(f"Resultado do Bind: {result}")
    if not result:
        print(f"Detalhes da falha: {conn.result}")
except Exception as e:
    print(f"Erro na conexao com AD: {e}")
