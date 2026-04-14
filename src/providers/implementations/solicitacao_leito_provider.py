from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.solicitacao_leito import SolicitacaoLeito
from typing import List, Optional

class SolicitacaoLeitoProvider:
    """
    Provider para abstrair o acesso a dados de SolicitacaoLeito no banco de dados SQLite.
    """
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def get_todas(self) -> List[SolicitacaoLeito]:
        result = await self.session.execute(
            select(SolicitacaoLeito).where(SolicitacaoLeito.status != "Cancelada")
        )
        return list(result.scalars().all())

    async def get_por_id(self, id: int) -> Optional[SolicitacaoLeito]:
        result = await self.session.execute(
            select(SolicitacaoLeito).where(SolicitacaoLeito.id == id)
        )
        return result.scalar_one_or_none()

    async def criar(self, data: dict) -> SolicitacaoLeito:
        solicitacao = SolicitacaoLeito(**data)
        self.session.add(solicitacao)
        await self.session.commit()
        await self.session.refresh(solicitacao)
        return solicitacao
        
    async def atualizar(self, id: int, data: dict) -> Optional[SolicitacaoLeito]:
        solicitacao = await self.get_por_id(id)
        if not solicitacao:
            return None
            
        for key, value in data.items():
            if hasattr(solicitacao, key):
                setattr(solicitacao, key, value)
                
        await self.session.commit()
        await self.session.refresh(solicitacao)
        return solicitacao
    
    async def deletar(self, id: int) -> bool:
        solicitacao = await self.get_por_id(id)
        if solicitacao:
            # Em vez de deletar fisicamente, podemos apenas marcar como Cancelada
            solicitacao.status = "Cancelada"
            await self.session.commit()
            return True
        return False
