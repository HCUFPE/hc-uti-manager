import os
import jwt
import re
import secrets
import sys
from datetime import datetime, timedelta
from abc import ABC, abstractmethod
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv

# Garantir que as variáveis de ambiente sejam carregadas ANTES de qualquer outra coisa
load_dotenv()

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from ldap3 import Server, Connection, ALL, SUBTREE, ALL_ATTRIBUTES
from ldap3.core.exceptions import LDAPBindError, LDAPSocketOpenError, LDAPException

from resources.database import get_app_db_session
from models.refresh_token import RefreshToken

# --- Configurações --- 
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_EXP_HOURS = int(os.getenv("JWT_EXP_HOURS", 24))
REFRESH_TOKEN_EXP_DAYS = int(os.getenv("REFRESH_TOKEN_EXP_DAYS", 30))
AUTH_ENABLED = os.getenv("AUTH_ENABLED", "true").lower() == "true"

# Torna o scheme opcional se AUTH_ENABLED=false
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login", auto_error=AUTH_ENABLED)

# --- Interface e Implementações de Provedor de Autenticação ---

class AuthProviderInterface(ABC):
    """Interface para provedores de autenticação."""
    @abstractmethod
    def authenticate_user(self, username, password) -> dict:
        pass

class MockAuthProvider(AuthProviderInterface):
    """Provedor de autenticação mock para desenvolvimento offline."""
    def authenticate_user(self, username, password) -> dict:
        print(f"SECURITY ALERT: Attempting MOCK authentication for user: {username}")
        # MOCK EXTREMAMENTE RESTRITIVO
        if username == "admin" and password == "admin_hc_uti_2024":
            print(f"SECURITY: Mock Authentication SUCCESSFUL for user: {username}")
            admin_group = "GLO-SEC-HCPE-SETISD"
            return {
                "username": "admin",
                "displayName": ["Mock Admin"],
                "groups": [admin_group, "Users"],
                "email": "admin@mock.com"
            }
        else:
            print(f"SECURITY: Mock Authentication FAILED for user: {username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Invalid credentials (MOCK)"
            )

class ActiveDirectoryAuthProvider(AuthProviderInterface):
    """Provedor de autenticação real usando LDAP/Active Directory."""
    def __init__(self):
        self.ad_url = os.getenv("AD_URL")
        self.ad_basedn = os.getenv("AD_BASEDN")
        self.ad_bind_user = os.getenv("AD_BIND_USER")
        self.ad_bind_password = os.getenv("AD_BIND_PASSWORD")
        if not self.ad_url or not self.ad_basedn:
            print("CRITICAL: AD_URL or AD_BASEDN not found in environment!")
            raise RuntimeError("Active Directory is not configured.")

    def _bind(self, user, password) -> Connection:
        print(f"DEBUG: LDAP Bind attempt: {user}")
        if not password:
            print(f"DEBUG: LDAP Bind FAILED: Empty password for {user}")
            raise LDAPBindError("Empty password not allowed")
            
        server = Server(self.ad_url, get_info=ALL)
        conn = Connection(
            server,
            user=user,
            password=password,
            receive_timeout=10,
        )
        if not conn.bind():
            print(f"DEBUG: LDAP Bind FAILED for {user}. Result: {conn.result}")
            raise LDAPBindError(f"Invalid credentials")
        
        print(f"DEBUG: LDAP Bind SUCCESS for {user}")
        return conn

    def authenticate_user(self, username, password) -> dict:
        print(f"--- Starting AD Authentication Process for: {username} ---")
        user_conn = None
        search_conn = None
        try:
            user_bind_dn = f"EBSERHNET\\{username}"
            # 1. Validar a senha do usuário IMEDIATAMENTE
            user_conn = self._bind(user_bind_dn, password)

            # 2. Se validou, agora busca os dados (usando conta de serviço ou a do próprio usuário)
            search_conn = user_conn
            if self.ad_bind_user and self.ad_bind_password:
                try:
                    search_conn = self._bind(self.ad_bind_user, self.ad_bind_password)
                except Exception as e:
                    print(f"WARNING: Service account bind failed, falling back to user bind: {e}")
                    search_conn = user_conn

            search_filter = f"(&(objectClass=user)(sAMAccountName={username}))"
            search_conn.search(
                search_base=self.ad_basedn,
                search_filter=search_filter,
                search_scope=SUBTREE,
                attributes=ALL_ATTRIBUTES,
                size_limit=1,
            )

            if not search_conn.entries:
                print(f"SECURITY: User {username} not found in AD search after successful bind.")
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found in directory")

            entry = search_conn.entries[0]
            attrs = entry.entry_attributes_as_dict
            user_info = {"username": username}

            groups_attr = attrs.get("memberOf") or []
            user_info["groups"] = [
                re.match(r"CN=([^,]+)", group).group(1)
                for group in groups_attr
                if re.match(r"CN=([^,]+)", group)
            ]

            for key, value in attrs.items():
                # Skip groups (already handled)
                if key == "memberOf":
                    continue
                
                # STRICT TYPE CHECKING: Only allow JSON-serializable primitives
                if isinstance(value, list):
                    # Only keep strings from lists, and ignore binary elements
                    clean_list = [str(v) for v in value if isinstance(v, (str, int, float, bool))]
                    if clean_list:
                        user_info[key] = clean_list
                elif isinstance(value, (str, int, float, bool)):
                    user_info[key] = value
                else:
                    # Log ignored field for debugging but don't break the flow
                    # print(f"DEBUG: Ignoring non-serializable field {key} of type {type(value)}")
                    pass

            print(f"SECURITY: AD Authentication SUCCESSFUL for user: {username}")
            return user_info

        except LDAPBindError:
            print(f"SECURITY: AD Authentication FAILED (Invalid Credentials) for: {username}")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        except (LDAPSocketOpenError, LDAPException) as e:
            print(f"ERROR: AD System Error for user {username}: {e}")
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Authentication server error")
        except Exception as e:
            import traceback
            print(f"CRITICAL: Unexpected error in authentication flow for user {username}:")
            traceback.print_exc()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal error: {str(e)}")
        finally:
            if search_conn and search_conn is not user_conn:
                search_conn.unbind()
            if user_conn:
                user_conn.unbind()

# --- AuthHandler Principal ---

class AuthHandler:
    def __init__(self):
        self._provider = None

    @property
    def provider(self) -> AuthProviderInterface:
        if self._provider is None:
            # Re-load env just in case something changed (e.g., in development)
            load_dotenv()
            ad_url = os.getenv("AD_URL")
            if ad_url and ad_url.strip():
                print(f"INFO: Initializing Active Directory Auth Provider (URL: {ad_url}).")
                self._provider = ActiveDirectoryAuthProvider()
            else:
                print("WARNING: AD_URL not found or empty. Initializing Mock Auth Provider.")
                self._provider = MockAuthProvider()
        return self._provider

    def authenticate_user(self, username, password):
        return self.provider.authenticate_user(username, password)

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if 'username' in to_encode:
            to_encode['sub'] = to_encode['username']
        expire = datetime.utcnow() + (expires_delta or timedelta(hours=JWT_EXP_HOURS))
        to_encode.update({"exp": expire})
        if not JWT_SECRET:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="JWT_SECRET not configured")
        return jwt.encode(to_encode, JWT_SECRET, algorithm="HS256")

    async def create_refresh_token(self, user_id: str, groups: list, db: AsyncSession) -> str:
        refresh_token_string = secrets.token_urlsafe(64)
        expires_at = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXP_DAYS)
        new_refresh_token = RefreshToken(user_id=user_id, token=refresh_token_string, groups=groups, expires_at=expires_at)
        db.add(new_refresh_token)
        await db.commit()
        return refresh_token_string

    async def verify_refresh_token(self, refresh_token: str, db: AsyncSession):
        stmt = select(RefreshToken).where(RefreshToken.token == refresh_token)
        result = await db.execute(stmt)
        token_obj = result.scalar_one_or_none()
        if not token_obj or token_obj.expires_at < datetime.utcnow():
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired refresh token")
        return token_obj

    async def invalidate_refresh_token(self, refresh_token: str, db: AsyncSession):
        stmt = delete(RefreshToken).where(RefreshToken.token == refresh_token)
        await db.execute(stmt)
        await db.commit()

    def decode_token(self, token: str = Depends(oauth2_scheme)):
        if not AUTH_ENABLED:
            return {
                "username": "dev_user",
                "groups": ["GLO-SEC-HCPE-SETISD", "Users"],
                "email": "dev@localhost"
            }
        
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
            
        try:
            if not JWT_SECRET:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="JWT_SECRET not configured")
            payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

# Instância única
auth_handler = AuthHandler()
