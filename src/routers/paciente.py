from fastapi import APIRouter, Depends
from typing import List

from controllers import paciente_controller
from dependencies import get_paciente_provider
from providers.interfaces.paciente_provider_interface import PacienteProviderInterface

from auth.auth import auth_handler

router = APIRouter(
    prefix="/api/pacientes",
    tags=["Pacientes"],
    dependencies=[Depends(auth_handler.decode_token)]
)

@router.get("", response_model=List[dict])
async def listar_pacientes(
    provider: PacienteProviderInterface = Depends(get_paciente_provider)
):
    """Lista todos os pacientes via PostgreSQL (AGHU)."""
    return await paciente_controller.listar_pacientes(provider)

@router.get("/{prontuario}", response_model=dict)
async def obter_paciente(
    prontuario: int,
    provider: PacienteProviderInterface = Depends(get_paciente_provider)
):
    """Obtém um paciente pelo prontuário via PostgreSQL (AGHU)."""
    return await paciente_controller.obter_paciente_por_prontuario(prontuario, provider)
