from sqlalchemy import Column, String, Integer, Boolean, DateTime
from sqlalchemy.sql import func
from resources.database import Base

class LeitoEstado(Base):
    """
    Armazena o estado local/extra de um leito que não existe no AGHU.
    Ex: Se a alta foi solicitada manualmente no sistema, ou se há uma reserva.
    """
    __tablename__ = "leito_estados"

    lto_id = Column(String(14), primary_key=True, index=True)
    alta_solicitada = Column(Boolean, default=False)
    
    # Dados da reserva (próximo paciente)
    prontuario_proximo = Column(Integer, nullable=True)
    idade_proximo = Column(Integer, nullable=True)
    especialidade_proximo = Column(String(100), nullable=True)
    solicitacao_id = Column(Integer, nullable=True) # ID da SolicitacaoLeito que originou a reserva
    
    atualizado_em = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def to_dict(self):
        return {
            "lto_id": self.lto_id,
            "alta_solicitada": self.alta_solicitada,
            "prontuario_proximo": self.prontuario_proximo,
            "idade_proximo": self.idade_proximo,
            "especialidade_proximo": self.especialidade_proximo,
            "solicitacao_id": self.solicitacao_id,
            "atualizado_em": self.atualizado_em
        }
