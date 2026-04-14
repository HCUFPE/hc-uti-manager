from typing import Dict, Any
from fastapi import HTTPException
from providers.implementations.indicadores_provider import IndicadoresProvider

class IndicadoresController:
    """
    Controller para formatar os dados de indicadores para o frontend.
    """

    def __init__(self, indicadores_provider: IndicadoresProvider):
        self.indicadores_provider = indicadores_provider

    async def obter_resumo(self) -> Dict[str, Any]:
        """Retorna o JSON consolidado das métricas de ocupação e fluxo."""
        try:
            dados = await self.indicadores_provider.get_indicadores_gerais()
            return dados
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao calcular indicadores: {str(e)}")
