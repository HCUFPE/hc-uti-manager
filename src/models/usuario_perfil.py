from sqlalchemy import Column, String, Integer
from resources.database import Base

class UsuarioPerfil(Base):
    """
    Armazena o perfil de acesso customizado para cada usuário do sistema.
    O login é validado no AD, mas o perfil é definido internamente.
    """
    __tablename__ = "usuarios_perfis"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    perfil = Column(String(50), nullable=False) 
    # Perfis: Administrador, UTI, NIR, Solicitante de Leito, Comum
    nome_completo = Column(String(100), nullable=True)
    lotacao = Column(String(100), nullable=True)
    email = Column(String(100), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "perfil": self.perfil,
            "nome_completo": self.nome_completo,
            "lotacao": self.lotacao,
            "email": self.email
        }
