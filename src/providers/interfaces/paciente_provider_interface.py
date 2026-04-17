from abc import ABC, abstractmethod
from typing import List, Dict, Any

class PacienteProviderInterface(ABC):
    """Interface (contrato) para provedores de dados de pacientes."""

    @abstractmethod
    async def listar_pacientes(self) -> List[Dict[str, Any]]:
        """Deve retornar uma lista de pacientes."""
        pass

    @abstractmethod
    async def obter_paciente_por_prontuario(self, prontuario: int) -> Dict[str, Any]:
        """Deve retornar um único paciente pelo seu prontuário."""
        pass
