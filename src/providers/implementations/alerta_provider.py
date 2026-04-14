from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from models.alerta import Alerta
from typing import List, Optional

class AlertaProvider:
    """
    Provider para gerenciar o acesso a dados de Alertas no banco de dados SQLite.
    """
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def get_todos(self) -> List[Alerta]:
        result = await self.session.execute(
            select(Alerta).order_by(Alerta.criado_em.desc())
        )
        return list(result.scalars().all())

    async def get_por_id(self, id: int) -> Optional[Alerta]:
        result = await self.session.execute(
            select(Alerta).where(Alerta.id == id)
        )
        return result.scalar_one_or_none()

    async def criar(self, data: dict) -> Alerta:
        alerta = Alerta(**data)
        self.session.add(alerta)
        await self.session.commit()
        await self.session.refresh(alerta)
        return alerta
        
    async def atualizar(self, id: int, data: dict) -> Optional[Alerta]:
        alerta = await self.get_por_id(id)
        if not alerta:
            return None
            
        for key, value in data.items():
            if hasattr(alerta, key):
                setattr(alerta, key, value)
                
        await self.session.commit()
        await self.session.refresh(alerta)
        return alerta

    async def deletar_todos(self) -> bool:
        """Utilitario para resetar alertas durante o job de sincronizacao (se necessario)"""
        # Em vez de deletar, poderíamos marcar como "resolvido" ou apagar os antigos
        await self.session.execute(delete(Alerta))
        await self.session.commit()
        return True
