from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.sql import func
from resources.database import Base

class SolicitacaoLeito(Base):
    """
    Representa uma solicitação de vaga/leito na UTI.
    """
    __tablename__ = "solicitacoes_leito"

    id = Column(Integer, primary_key=True, autoincrement=True)
    prontuario = Column(String(50), nullable=False)
    idade = Column(Integer, nullable=False)
    especialidade = Column(String(100), nullable=False)
    tipo = Column(String(50), nullable=False) # Ex: Cirurgico, HEM, Obstetrico, UTI
    status = Column(String(50), default="Pendente") # Pendente, Reservado, Cancelada
    turno = Column(String(50), nullable=False) # Manha, Tarde, Noite
    destino = Column(String(100), nullable=True) # Ex: Leito 05
    
    criado_em = Column(DateTime, server_default=func.now())
    atualizado_em = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "prontuario": self.prontuario,
            "idade": self.idade,
            "especialidade": self.especialidade,
            "tipo": self.tipo,
            "status": self.status,
            "turno": self.turno,
            "destino": self.destino,
            "criado_em": self.criado_em.isoformat() if self.criado_em else None,
            "atualizado_em": self.atualizado_em.isoformat() if self.atualizado_em else None,
        }
