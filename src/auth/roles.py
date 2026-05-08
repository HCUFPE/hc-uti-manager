from enum import Enum

class Role(str, Enum):
    ADMIN = "Administrador"
    UTI_ADMIN = "UTI-Admin"
    NIR_ADMIN = "NIR-Admin"
    COB_ADMIN = "COB-Admin"
    BC_ADMIN = "BC-Admin"
    HEM_ADMIN = "HEM-Admin"
    UTI = "UTI"
    NIR = "NIR"
    COB = "COB"
    BC = "BC"
    HEM = "HEM"
    COMUM = "Comum"

def has_role(user_perfil: str, required_role: Role) -> bool:
    """
    Verifica se o usuário possui o papel necessário.
    Administrador sempre tem acesso a tudo.
    """
    if user_perfil == Role.ADMIN:
        return True
    return user_perfil == required_role
