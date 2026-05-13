import os
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

# Interfaces
from providers.interfaces.paciente_provider_interface import PacienteProviderInterface
from providers.interfaces.leito_provider_interface import LeitoProviderInterface

# Implementations
from providers.implementations.paciente_postgres_provider import PacientePostgresProvider
from providers.implementations.banco_aghu.leito_aghu_provider import LeitoAghuProvider
from providers.implementations.leito_estado_provider import LeitoEstadoProvider
from providers.implementations.solicitacao_alta_provider import SolicitacaoAltaProvider
from providers.implementations.solicitacao_leito_provider import SolicitacaoLeitoProvider
from providers.implementations.alerta_provider import AlertaProvider
from providers.implementations.historico_provider import HistoricoProvider
from providers.implementations.indicadores_provider import IndicadoresProvider

# Controllers
from controllers.leitos_controller import LeitosController
from controllers.altas_controller import AltasController
from controllers.solicitacao_leito_controller import SolicitacaoLeitoController
from controllers.alerta_controller import AlertaController
from controllers.indicadores_controller import IndicadoresController

# Resources
from resources.database import get_aghu_db_session, get_app_db_session

# --- PACIENTES -----------------------------------------------------------

def get_paciente_provider(
    session: AsyncSession = Depends(get_aghu_db_session)
) -> PacienteProviderInterface:
    """Provedor de pacientes via PostgreSQL (AGHU)."""
    return PacientePostgresProvider(session=session)

# --- LEITOS --------------------------------------------------------------

def _get_leito_aghu_provider(
    session: AsyncSession = Depends(get_aghu_db_session)
) -> LeitoProviderInterface:
    return LeitoAghuProvider(session=session)

def get_leito_estado_provider(
    session: AsyncSession = Depends(get_app_db_session)
) -> LeitoEstadoProvider:
    """Provedor para o estado local (SQLite)."""
    return LeitoEstadoProvider(session=session)

def get_solicitacao_alta_provider(
    session: AsyncSession = Depends(get_app_db_session)
) -> SolicitacaoAltaProvider:
    return SolicitacaoAltaProvider(session=session)

def get_solicitacao_leito_provider(
    session: AsyncSession = Depends(get_app_db_session)
) -> SolicitacaoLeitoProvider:
    return SolicitacaoLeitoProvider(session=session)

def get_leito_controller(
    census_provider: LeitoProviderInterface = Depends(_get_leito_aghu_provider),
    estado_provider: LeitoEstadoProvider = Depends(get_leito_estado_provider),
    alta_provider: SolicitacaoAltaProvider = Depends(get_solicitacao_alta_provider),
    solicitacao_provider: SolicitacaoLeitoProvider = Depends(get_solicitacao_leito_provider)
) -> LeitosController:
    """
    Constrói o controller injetando as três fontes de dados:
    - census_provider: dados em tempo real do AGHU (PostgreSQL)
    - estado_provider: estado local persistido (SQLite) - Reservas
    - alta_provider: solicitações de alta ricas (SQLite)
    """
    return LeitosController(census_provider, estado_provider, alta_provider, solicitacao_provider)

# --- HISTORICO --------------------------------------------------

def get_historico_provider(
    session: AsyncSession = Depends(get_app_db_session),
) -> HistoricoProvider:
    """Provedor para registro e consulta do histórico de ações."""
    return HistoricoProvider(session=session)

# --- ALTAS --------------------------------------------------------------

def get_altas_controller(
    alta_provider: SolicitacaoAltaProvider = Depends(get_solicitacao_alta_provider),
    leitos_controller: LeitosController = Depends(get_leito_controller),
    estado_provider: LeitoEstadoProvider = Depends(get_leito_estado_provider),
    historico_provider: HistoricoProvider = Depends(get_historico_provider)
) -> AltasController:
    return AltasController(alta_provider, leitos_controller, estado_provider, historico_provider)

# --- SOLICITACOES LEITO --------------------------------------------------

def get_solicitacao_leito_controller(
    leito_provider: SolicitacaoLeitoProvider = Depends(get_solicitacao_leito_provider),
    estado_provider: LeitoEstadoProvider = Depends(get_leito_estado_provider),
    historico_provider: HistoricoProvider = Depends(get_historico_provider)
) -> SolicitacaoLeitoController:
    return SolicitacaoLeitoController(leito_provider, estado_provider, historico_provider)

# --- ALERTAS --------------------------------------------------

def get_alerta_provider(
    session: AsyncSession = Depends(get_app_db_session)
) -> AlertaProvider:
    return AlertaProvider(session=session)

def get_alerta_controller(
    alerta_provider: AlertaProvider = Depends(get_alerta_provider),
    leitos_controller: LeitosController = Depends(get_leito_controller),
    alta_provider: SolicitacaoAltaProvider = Depends(get_solicitacao_alta_provider),
    solicitacao_leito_provider: SolicitacaoLeitoProvider = Depends(get_solicitacao_leito_provider),
    historico_provider: HistoricoProvider = Depends(get_historico_provider)
) -> AlertaController:
    return AlertaController(alerta_provider, leitos_controller, alta_provider, solicitacao_leito_provider, historico_provider)

# --- INDICADORES --------------------------------------------------

def get_indicadores_provider(
    session: AsyncSession = Depends(get_app_db_session),
    census_provider: LeitoProviderInterface = Depends(_get_leito_aghu_provider)
) -> IndicadoresProvider:
    return IndicadoresProvider(session=session, census_provider=census_provider)

def get_indicadores_controller(
    indicadores_provider: IndicadoresProvider = Depends(get_indicadores_provider)
) -> IndicadoresController:
    return IndicadoresController(indicadores_provider)


from auth.roles import Role
from auth.auth import auth_handler
from fastapi import HTTPException, status
import logging
from typing import List

logger = logging.getLogger(__name__)

# --- SEGURANÇA E RBAC -----------------------------------------------------------

class RoleChecker:
    def __init__(self, allowed_roles: List[Role]):
        self.allowed_roles = allowed_roles

    async def __call__(self, current_user: dict = Depends(auth_handler.decode_token)):
        if current_user.get("perfil") not in self.allowed_roles:
            logger.warning(f"Acesso negado: Usuário {current_user.get('username')} (Perfil: {current_user.get('perfil')}) tentou acessar recurso restrito a {self.allowed_roles}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Você não tem permissão para realizar esta operação."
            )
        return current_user

def check_role(allowed_roles: List[Role]):
    return RoleChecker(allowed_roles)
