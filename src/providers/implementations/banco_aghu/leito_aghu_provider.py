import os
from typing import List, Dict, Any
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from providers.interfaces.leito_provider_interface import LeitoProviderInterface

def get_sql_query(file_path: str) -> str:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Path: src/providers/implementations/banco_aghu/../../sql/leito/file_path
    # Resolves to: src/providers/sql/leito/file_path
    sql_file_path = os.path.join(base_dir, '..', '..', 'sql', 'leito', file_path)
    try:
        with open(sql_file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        # Fallback for different execution contexts
        alt_path = os.path.join('src', 'providers', 'sql', 'leito', file_path)
        if os.path.exists(alt_path):
            with open(alt_path, 'r', encoding='utf-8') as f:
                return f.read()
        raise RuntimeError(f"Arquivo SQL não encontrado em: {sql_file_path}")

class LeitoAghuProvider(LeitoProviderInterface):
    """
    Provedor de dados de leitos que consulta diretamente o banco de dados AGHU (Postgres).
    Foca na leitura do censo em tempo real.
    """
    def __init__(self, session: AsyncSession):
        self.session = session

    async def listar_leitos(self) -> List[Dict[str, Any]]:
        """Busca o censo de leitos ativos na UTI (unf_seq=115)."""
        query_text = get_sql_query('censo_leitos.sql')
        result = await self.session.execute(text(query_text))
        rows = result.mappings().all()
        return [dict(r) for r in rows]

    async def listar_leitos_disponiveis_para_reserva(self) -> List[Dict[str, Any]]:
        """
        Retorna leitos ocupados que podem vir a ser reservados.
        Nota: A lógica de 'alta solicitada' será integrada via Local State no Controller.
        """
        leitos = await self.listar_leitos()
        # Filtro inicial: apenas leitos ocupados podem ter alta solicitada
        return [l for l in leitos if l['status'] == 'OCUPADO']

    async def solicitar_alta(self, leito_id: str) -> None:
        """Operação de escrita será gerenciada pelo Local State Provider."""
        pass

    async def cancelar_alta(self, leito_id: str) -> None:
        """Operação de escrita será gerenciada pelo Local State Provider."""
        pass
