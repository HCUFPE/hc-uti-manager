from sqlalchemy import Column, String, Integer, DateTime, Boolean
from sqlalchemy.sql import func
from datetime import timedelta
from resources.database import Base

class SolicitacaoLeito(Base):
    """
    Representa uma solicitação de vaga/leito na UTI.
    """
    __tablename__ = "solicitacoes_leito"

    id = Column(Integer, primary_key=True, autoincrement=True)
    prontuario = Column(String(50), nullable=False)
    nome = Column(String(150), nullable=True) # Nome completo do paciente
    idade = Column(Integer, nullable=False)
    especialidade = Column(String(100), nullable=False)
    procedimento = Column(String(250), nullable=True) # Descrição do procedimento principal
    tipo = Column(String(50), nullable=False) # Ex: Cirurgico, HEM, Obstetrico, UTI
    status = Column(String(50), default="Pendente") # Pendente, Reservado, Cancelada
    turno = Column(String(50), nullable=False) # Manha, Tarde, Noite
    data_cirurgia = Column(String(20), nullable=True) # Data prevista (DD-MM-YYYY)
    hora_cirurgia = Column(String(5), nullable=True) # Hora prevista de início (HH:MM)
    destino = Column(String(100), nullable=True) # Ex: Leito 05
    prioridade = Column(String(10), nullable=True) # P1, P2, P3, P4, P5
    prioridade_manual = Column(Boolean, default=False, server_default="0", nullable=False)
    perfil_solicitante = Column(String(50), nullable=True) # COB, BC, HEM, UTI, etc.
    
    cirurgia_finalizada = Column(Boolean, default=False)
    encaminhamento_liberado = Column(Boolean, default=False)
    cirurgia_finalizada_em = Column(DateTime, nullable=True)
    encaminhamento_liberado_em = Column(DateTime, nullable=True)
    
    criado_em = Column(DateTime, server_default=func.now())
    atualizado_em = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def to_dict(self):
        # Ajuste para horário de Brasília (-3h)
        criado_local = (self.criado_em - timedelta(hours=3)) if self.criado_em else None
        atualizado_local = (self.atualizado_em - timedelta(hours=3)) if self.atualizado_em else None
        cirurgia_finalizada_local = (self.cirurgia_finalizada_em - timedelta(hours=3)) if self.cirurgia_finalizada_em else None
        encaminhamento_liberado_local = (self.encaminhamento_liberado_em - timedelta(hours=3)) if self.encaminhamento_liberado_em else None
        
        return {
            "id": self.id,
            "prontuario": self.prontuario,
            "nome": self.nome,
            "idade": self.idade,
            "especialidade": self.especialidade,
            "procedimento": self.procedimento,
            "tipo": self.tipo,
            "status": self.status,
            "turno": self.turno,
            "data_cirurgia": self.data_cirurgia,
            "hora_cirurgia": self.hora_cirurgia,
            "prioridade": self.prioridade,
            "prioridade_manual": bool(self.prioridade_manual),
            "destino": self.destino,
            "perfil_solicitante": self.perfil_solicitante,
            "cirurgia_finalizada": bool(self.cirurgia_finalizada),
            "encaminhamento_liberado": bool(self.encaminhamento_liberado),
            "cirurgia_finalizada_em": cirurgia_finalizada_local.isoformat() if cirurgia_finalizada_local else None,
            "encaminhamento_liberado_em": encaminhamento_liberado_local.isoformat() if encaminhamento_liberado_local else None,
            "criado_em": criado_local.isoformat() if criado_local else None,
            "atualizado_em": updated_local.isoformat() if (updated_local := atualizado_local) else None,
        }
