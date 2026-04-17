from enum import Enum
from typing import List

class Role(str, Enum):
    ADMIN = "admin"
    COORDINATION = "coordination"
    ASSISTENTIAL = "assistential"

# Mapeamento de Grupos do AD para Papéis do Sistema
# Adicione aqui os nomes exatos dos grupos retornados pelo LDAP/EBSERH
ROLE_GROUPS = {
    Role.ADMIN: [
        "GLO-SEC-HCPE-SETISD",  # Grupo de TI/Sistemas
        "TI-ADMIN"
    ],
    Role.COORDINATION: [
        "COORD-UTI-MEDICA",
        "COORD-UTI-ENFERMAGEM",
        "CHEFIA-UTI"
    ],
    Role.ASSISTENTIAL: [
        "Users",
        "MEDICOS",
        "ENFERMEIROS",
        "FISIOTERAPEUTAS"
    ]
}

def get_user_role(user_groups: List[str]) -> Role:
    """
    Identifica o papel de maior privilégio do usuário baseado nos seus grupos.
    """
    # Ordem de precedência: Admin > Coordenação > Assistencial
    if any(group in user_groups for group in ROLE_GROUPS[Role.ADMIN]):
        return Role.ADMIN
    if any(group in user_groups for group in ROLE_GROUPS[Role.COORDINATION]):
        return Role.COORDINATION
    
    return Role.ASSISTENTIAL
