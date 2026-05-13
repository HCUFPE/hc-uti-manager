import asyncio
import os
import sys

# Adiciona o diretório src ao path
sys.path.append(os.path.abspath('src'))

from controllers.leitos_controller import LeitosController
from providers.implementations.leito_aghu_provider import LeitoAghuProvider
from providers.implementations.leito_estado_provider import LeitoEstadoProvider
from providers.implementations.solicitacao_alta_provider import SolicitacaoAltaProvider
from providers.implementations.solicitacao_leito_provider import SolicitacaoLeitoProvider

async def test():
    # Setup manual das dependências para teste rápido
    from resources.database import async_session
    async with async_session() as session:
        census = LeitoAghuProvider()
        estado = LeitoEstadoProvider(session)
        alta = SolicitacaoAltaProvider(session)
        sol = SolicitacaoLeitoProvider(session)
        
        controller = LeitosController(census, estado, alta, sol)
        leitos = await controller.listar_leitos()
        
        uti02 = next((l for l in leitos if l['lto_lto_id'] == 'UTI-02'), None)
        print(f"DEBUG UTI-02: {uti02}")

if __name__ == "__main__":
    asyncio.run(test())
