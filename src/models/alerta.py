from sqlalchemy import Column, String, Integer, Boolean, DateTime
from datetime import datetime, timedelta
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
    perfil_alvo = Column(String(50), nullable=True) # Se nulo, visível para UTI/NIR/Admin

    criado_em = Column(DateTime, default=datetime.utcnow)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        # Ajuste para horário de Brasília (-3h)
        data_local = (self.criado_em - timedelta(hours=3)) if self.criado_em else None
        
        return {
            "id": str(self.id),
            "tipo": self.tipo,
            "categoria": self.categoria,
            "titulo": self.titulo,
            "mensagem": self.mensagem,
            "dataHora": data_local.strftime("%d/%m/%Y %H:%M") if data_local else "",
            "lido": self.lido,
            "lto_id": self.lto_id,
            "prontuario": self.prontuario,
            "perfil_alvo": self.perfil_alvo
        }
