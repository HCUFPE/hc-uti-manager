from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.solicitacao_alta import SolicitacaoAlta
from typing import List, Optional

class SolicitacaoAltaProvider:
    """
    Provider para abstrair o acesso a dados de SolicitacaoAlta no banco de dados SQLite.
    """
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def obter_altas_map(self) -> dict:
        result = await self.session.execute(
            select(SolicitacaoAlta).where(SolicitacaoAlta.status.in_(["pendente", "definida"]))
        )
        return {a.lto_id: a for a in result.scalars().all()}

    async def get_todas(self) -> List[SolicitacaoAlta]:
        result = await self.session.execute(select(SolicitacaoAlta))
        return list(result.scalars().all())

    async def get_por_id(self, id: int) -> Optional[SolicitacaoAlta]:
        result = await self.session.execute(
            select(SolicitacaoAlta).where(SolicitacaoAlta.id == id)
        )
        return result.scalar_one_or_none()
    
    async def get_por_lto_id(self, lto_id: str) -> Optional[SolicitacaoAlta]:
        # Consideramos apenas a mais recente "pendente" ou "definida" para o leito
        result = await self.session.execute(
            select(SolicitacaoAlta)
            .where(SolicitacaoAlta.lto_id == lto_id)
            .where(SolicitacaoAlta.status.in_(["pendente", "definida"]))
            .order_by(SolicitacaoAlta.criado_em.desc())
        )
        return result.scalar_one_or_none()

    async def criar(self, data: dict) -> SolicitacaoAlta:
        solicitacao = SolicitacaoAlta(**data)
        self.session.add(solicitacao)
        await self.session.commit()
        await self.session.refresh(solicitacao)
        return solicitacao
        
    async def atualizar(self, id: int, data: dict) -> Optional[SolicitacaoAlta]:
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
            solicitacao.status = "cancelada"
            await self.session.commit()
            return True
        return False
