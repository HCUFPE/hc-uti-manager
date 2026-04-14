from sqlalchemy import Column, String, Integer, Boolean, DateTime
from sqlalchemy.sql import func
from resources.database import Base

class Alerta(Base):
    """
    Representa um alerta ou notificação gerada pelo sistema.
    """
    __tablename__ = "alertas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tipo = Column(String(50), nullable=False) # critico, aviso, info
    categoria = Column(String(50), nullable=False) # Infeccioso, Permanencia, Gargalo, Limpeza, Outros
    titulo = Column(String(255), nullable=False)
    mensagem = Column(String(1000), nullable=False)
    lido = Column(Boolean, default=False, nullable=False)
    
    # Identificadores opcionais para linkar o alerta a um objeto específico
    lto_id = Column(String(14), nullable=True) 
    prontuario = Column(String(50), nullable=True)

    criado_em = Column(DateTime, server_default=func.now())
    atualizado_em = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def to_dict(self):
        return {
            "id": str(self.id),
            "tipo": self.tipo,
            "categoria": self.categoria,
            "titulo": self.titulo,
            "mensagem": self.mensagem,
            "lido": self.lido,
            "lto_id": self.lto_id,
            "prontuario": self.prontuario,
            "dataHora": self.criado_em.strftime("%Y-%m-%d %H:%M") if self.criado_em else None,
            "atualizado_em": self.atualizado_em.isoformat() if self.atualizado_em else None,
        }
