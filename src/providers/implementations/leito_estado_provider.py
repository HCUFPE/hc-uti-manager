from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.leito_estado import LeitoEstado
from typing import Dict, Any, List

class LeitoEstadoProvider:
    """
    Gerencia o estado extra dos leitos no banco local (SQLite).
    """
    def __init__(self, session: AsyncSession):
        self.session = session

    async def obter_estados(self) -> Dict[str, LeitoEstado]:
        """Retorna um mapeamento de lto_id para o objeto LeitoEstado."""
        result = await self.session.execute(select(LeitoEstado))
        estados = result.scalars().all()
        return {e.lto_id: e for e in estados}

        await self.session.commit()

    async def salvar_alta(self, lto_id: str, solicitada: bool):
        """Salva o estado de alta solicitada para um leito."""
        result = await self.session.execute(select(LeitoEstado).where(LeitoEstado.lto_id == lto_id))
        estado = result.scalar_one_or_none()
        
        if not estado:
            estado = LeitoEstado(lto_id=lto_id, alta_solicitada=solicitada)
            self.session.add(estado)
        else:
            estado.alta_solicitada = solicitada
            
        await self.session.commit()

    async def limpar_reserva(self, lto_id: str) -> int | None:

        await self.session.commit()

    async def limpar_reserva(self, lto_id: str) -> int | None:
        """Limpa os campos de reserva de um leito e retorna o solicitacao_id que estava vinculado."""
        result = await self.session.execute(select(LeitoEstado).where(LeitoEstado.lto_id == lto_id))
        estado = result.scalar_one_or_none()
        
        if estado:
            sol_id = estado.solicitacao_id
            estado.prontuario_proximo = None
            estado.idade_proximo = None
            estado.especialidade_proximo = None
            estado.solicitacao_id = None
            await self.session.commit()
            return sol_id
        return None
