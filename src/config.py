import os
import sys
import logging
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import model_validator

logger = logging.getLogger("config")

class Settings(BaseSettings):
    ENVIRONMENT: str = "development"
    SECRET_KEY: str = "secret-key-change-in-production-123456789"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480

    # Banco de Dados
    POSTGRES_DSN: Optional[str] = None
    SQLITE_DSN: Optional[str] = None
    SQLITE_PATH: Optional[str] = "data/app.db"

    # Integrações
    AGHU_API_URL: Optional[str] = None
    LDAP_SERVER: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @model_validator(mode="after")
    def validar_segredos_producao(self):
        env = (self.ENVIRONMENT or "").lower()
        if env == "production":
            segredos_fracos = [
                "secret-key-change-in-production-123456789",
                "secret",
                "123456",
                "admin",
                "change_me",
                "hc-uti-secret"
            ]
            if not self.SECRET_KEY or self.SECRET_KEY.lower() in segredos_fracos or len(self.SECRET_KEY) < 16:
                raise ValueError(
                    "CRITICAL SECURITY ERROR: SECRET_KEY inválida ou muito fraca para ambiente de PRODUÇÃO. "
                    "Configure uma chave forte com pelo menos 16 caracteres no arquivo .env."
                )
        return self

settings = Settings()
