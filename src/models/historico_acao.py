"""Modelo SQLAlchemy para o Histórico de Ações do sistema."""

from datetime import datetime, timedelta
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
        # Ajuste para horário de Brasília (-3h)
        data_local = (self.criado_em - timedelta(hours=3)) if self.criado_em else None
        
        return {
            "id": str(self.id),
            "criado_em": self.criado_em,
            "operador": self.operador,
            "tipo": self.tipo,
            "acao": self.acao,
            "detalhes": self.detalhes or "",
            "dataHora": data_local.strftime("%d/%m/%Y %H:%M") if data_local else "",
        }
