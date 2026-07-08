from sqlalchemy import Column, Float, Date
from resources.database import Base

class HistoricoOcupacao(Base):
    """
    Representa o registro consolidado da taxa de ocupação diária da UTI.
    """
    __tablename__ = "historico_ocupacao"

    data = Column(Date, primary_key=True)
    taxa_ocupacao = Column(Float, nullable=False)

    def to_dict(self):
        return {
            "data": self.data.isoformat() if self.data else None,
            "taxa_ocupacao": self.taxa_ocupacao
        }
