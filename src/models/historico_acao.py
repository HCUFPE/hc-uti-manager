"""Modelo SQLAlchemy para o Histórico de Ações do sistema."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from resources.database import Base


class HistoricoAcao(Base):
    """Registra cada ação realizada pelos usuários no sistema."""

    __tablename__ = "historico_acoes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    operador = Column(String, nullable=False, index=True)
    tipo = Column(String, nullable=False, index=True)  # alta | reserva | destino | cancelamento | solicitacao | status
    acao = Column(String, nullable=False)
    detalhes = Column(String, nullable=True)
    criado_em = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "operador": self.operador,
            "tipo": self.tipo,
            "acao": self.acao,
            "detalhes": self.detalhes or "",
            "dataHora": self.criado_em.strftime("%Y-%m-%d %H:%M") if self.criado_em else "",
        }
