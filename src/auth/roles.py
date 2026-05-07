from enum import Enum

class Role(str, Enum):
    ADMIN = "Administrador"
    UTI = "UTI"
    NIR = "NIR"
    SOLICITANTE = "Solicitante de Leito"
    COMUM = "Comum"

def has_role(user_perfil: str, required_role: Role) -> bool:
    """
    Verifica se o usuário possui o papel necessário.
    Administrador sempre tem acesso a tudo.
    """
    if user_perfil == Role.ADMIN:
        return True
    return user_perfil == required_role
