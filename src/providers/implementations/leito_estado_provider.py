from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.leito_estado import LeitoEstado
from typing import Dict, Any, List, Optional

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

    async def salvar_reserva(
        self,
        lto_id: str,
        prontuario: int,
        idade: int,
        especialidade: str,
        solicitacao_id: Optional[int] = None,
    ) -> None:
        """Salva ou atualiza os dados de reserva (próximo paciente) para um leito."""
        result = await self.session.execute(select(LeitoEstado).where(LeitoEstado.lto_id == lto_id))
        estado = result.scalar_one_or_none()

        if not estado:
            estado = LeitoEstado(lto_id=lto_id)
            self.session.add(estado)

        estado.prontuario_proximo = prontuario
        estado.idade_proximo = idade
        estado.especialidade_proximo = especialidade
        if solicitacao_id is not None:
            estado.solicitacao_id = solicitacao_id

        await self.session.commit()

    async def limpar_reserva(self, lto_id: str) -> Dict[str, Any]:
        """Limpa os campos de reserva de um leito e retorna os dados vinculados."""
        result = await self.session.execute(select(LeitoEstado).where(LeitoEstado.lto_id == lto_id))
        estado = result.scalar_one_or_none()

        data = {"sol_id": None, "prontuario": None}
        if estado:
            data["sol_id"] = estado.solicitacao_id
            data["prontuario"] = estado.prontuario_proximo
            
            estado.prontuario_proximo = None
            estado.idade_proximo = None
            estado.especialidade_proximo = None
            estado.solicitacao_id = None
            await self.session.commit()
            
        return data

    async def limpar_reserva_por_solicitacao(self, sol_id: int) -> bool:
        """Limpa a reserva de qualquer leito que esteja vinculado a esta solicitação."""
        result = await self.session.execute(
            select(LeitoEstado).where(LeitoEstado.solicitacao_id == sol_id)
        )
        estado = result.scalar_one_or_none()
        
        if estado:
            estado.prontuario_proximo = None
            estado.idade_proximo = None
            estado.especialidade_proximo = None
            estado.solicitacao_id = None
            await self.session.commit()
            return True
        return False

    async def atualizar_dados_reserva_por_solicitacao(self, sol_id: int, prontuario: int, idade: int, especialidade: str) -> bool:
        """Atualiza os dados da reserva de um leito baseado na edição da solicitação."""
        result = await self.session.execute(
            select(LeitoEstado).where(LeitoEstado.solicitacao_id == sol_id)
        )
        estado = result.scalar_one_or_none()
        
        if estado:
            if prontuario is not None:
                estado.prontuario_proximo = prontuario
            estado.idade_proximo = idade
            estado.especialidade_proximo = especialidade
            await self.session.commit()
            return True
        return False
