from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.sql import func
from resources.database import Base

class SolicitacaoAlta(Base):
    """
    Representa uma solicitação de alta médica de um paciente da UTI para outro leito/setor.
    """
    __tablename__ = "solicitacoes_alta"

    id = Column(Integer, primary_key=True, autoincrement=True)
    lto_id = Column(String(14), index=True, nullable=False)
    prontuario = Column(String(50), nullable=False)
    leito_destino = Column(String(100), nullable=True)
    necessidades_especiais = Column(String(255), nullable=True)
    status = Column(String(50), default="pendente")
    
    criado_em = Column(DateTime, server_default=func.now())
    atualizado_em = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "lto_id": self.lto_id,
            "prontuario": self.prontuario,
            "leito_destino": self.leito_destino,
            "necessidades_especiais": self.necessidades_especiais,
            "status": self.status,
            "criado_em": self.criado_em.isoformat() if self.criado_em else None,
            "atualizado_em": self.atualizado_em.isoformat() if self.atualizado_em else None,
        }
