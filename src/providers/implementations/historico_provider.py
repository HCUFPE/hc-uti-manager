"""Provider para persistência e consulta do Histórico de Ações."""

from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from models.historico_acao import HistoricoAcao


class HistoricoProvider:
    """Gerencia o registro e a consulta de ações no banco local (SQLite)."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def registrar(
        self,
        operador: str,
        tipo: str,
        acao: str,
        detalhes: Optional[str] = None,
    ) -> HistoricoAcao:
        """Persiste uma nova entrada no histórico.

        Args:
            operador: Username ou nome do usuário que realizou a ação.
            tipo: Categoria da ação (alta, reserva, destino, cancelamento, solicitacao, status).
            acao: Descrição curta da ação realizada.
            detalhes: Informação complementar (prontuário, leito, etc).

        Returns:
            O objeto HistoricoAcao criado.
        """
        entrada = HistoricoAcao(
            operador=operador,
            tipo=tipo,
            acao=acao,
            detalhes=detalhes,
        )
        self.session.add(entrada)
        await self.session.commit()
        await self.session.refresh(entrada)
        return entrada

    async def listar(
        self,
        limit: int = 100,
        offset: int = 0,
        tipo: Optional[str] = None,
        operador: Optional[str] = None,
        busca: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Retorna entradas do histórico, ordenadas da mais recente para a mais antiga.

        Args:
            limit: Máximo de registros a retornar.
            offset: Deslocamento para paginação.
            tipo: Filtra pelo tipo da ação.
            operador: Filtra por nome do operador.
            busca: Pesquisa livre em acao, detalhes e operador.

        Returns:
            Lista de dicionários com os dados das ações.
        """
        stmt = select(HistoricoAcao)

        if tipo:
            stmt = stmt.where(HistoricoAcao.tipo == tipo)
        if operador:
            stmt = stmt.where(HistoricoAcao.operador.ilike(f"%{operador}%"))
        if busca:
            termo = f"%{busca}%"
            stmt = stmt.where(
                HistoricoAcao.acao.ilike(termo)
                | HistoricoAcao.detalhes.ilike(termo)
                | HistoricoAcao.operador.ilike(termo)
            )

        stmt = stmt.order_by(desc(HistoricoAcao.criado_em)).limit(limit).offset(offset)

        result = await self.session.execute(stmt)
        return [h.to_dict() for h in result.scalars().all()]
