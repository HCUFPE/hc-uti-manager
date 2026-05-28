from typing import List, Dict, Any
import os
from fastapi import HTTPException, status

from providers.interfaces.paciente_provider_interface import PacienteProviderInterface

MOCK_PATIENTS = [
    {
        "prontuario": 77,
        "nome": "MANOEL SEVERINO DOS SANTOS",
        "dt_nascimento": "1927-05-15",
        "sexo": "M",
        "cor": "Branca",
        "nome_mae": "Maria dos Santos",
        "nome_pai": "Jose dos Santos"
    },
    {
        "prontuario": 123,
        "nome": "ANA MARIA SILVA",
        "dt_nascimento": "1992-10-10",
        "sexo": "F",
        "cor": "Parda",
        "nome_mae": "Maria da Silva",
        "nome_pai": "Joao da Silva"
    },
    {
        "prontuario": 999999,
        "nome": "PACIENTE TESTE ALTA",
        "dt_nascimento": "1981-06-20",
        "sexo": "M",
        "cor": "Branca",
        "nome_mae": "Maria de Teste",
        "nome_pai": "Pai de Teste"
    },
    {
        "prontuario": 123456,
        "nome": "PACIENTE ATUAL",
        "dt_nascimento": "1990-01-01",
        "sexo": "M",
        "cor": "Parda",
        "nome_mae": "Mae de Teste",
        "nome_pai": "Pai de Teste"
    }
]

async def listar_pacientes(
    provider: PacienteProviderInterface
) -> List[Dict[str, Any]]:
    if os.getenv("MOCK_BEDS") == "true":
        return MOCK_PATIENTS
    return await provider.listar_pacientes()

async def obter_paciente_por_prontuario(
    prontuario: int,
    provider: PacienteProviderInterface
) -> Dict[str, Any]:
    if os.getenv("MOCK_BEDS") == "true":
        p = next((x for x in MOCK_PATIENTS if x["prontuario"] == prontuario), None)
        if not p:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Paciente não encontrado (MOCK)"
            )
        return p
    return await provider.obter_paciente_por_prontuario(prontuario)
