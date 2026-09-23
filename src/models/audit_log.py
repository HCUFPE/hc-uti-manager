from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from resources.database import Base
from enum import Enum as PyEnum

class CategoriaAuditoria(str, PyEnum):
    SEGURANCA = "SEGURANCA"
    NEGOCIO_CLINICO = "NEGOCIO_CLINICO"
    CONFIGURACAO = "CONFIGURACAO"

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, server_default=func.now(), nullable=False, index=True)
    categoria = Column(String(50), nullable=False, default=CategoriaAuditoria.NEGOCIO_CLINICO, index=True)
    acao = Column(String(100), nullable=False, index=True)
    usuario_id = Column(String(100), nullable=True, index=True)
    ip_origem = Column(String(45), nullable=True)  # Suporta IPv4 e IPv6
    detalhes = Column(Text, nullable=True)
    estado_anterior = Column(Text, nullable=True)  # JSON serializado
    estado_novo = Column(Text, nullable=True)      # JSON serializado
