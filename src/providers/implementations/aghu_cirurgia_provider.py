import os
from typing import Dict, Any, Optional
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

def get_sql_query(file_path: str) -> str:
    """Carrega o conteúdo de um arquivo SQL de template.

    Args:
        file_path (str): Nome do arquivo SQL.

    Returns:
        str: Conteúdo do arquivo SQL.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    sql_file_path = os.path.join(base_dir, '..', 'sql', 'solicitacao', file_path)
    try:
        with open(sql_file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        raise RuntimeError(f"Arquivo SQL não encontrado em: {sql_file_path}")


class AghuCirurgiaProvider:
    """Provider para consultar informações de cirurgias do AGHU."""

    def __init__(self, session: AsyncSession):
        """Inicializa o provider com uma sessão do SQLAlchemy.

        Args:
            session (AsyncSession): Sessão assíncrona do banco de dados.
        """
        self.session = session

    async def obter_cirurgia_por_prontuario(self, prontuario: str) -> Optional[Dict[str, Any]]:
        """Busca no AGHU a cirurgia programada ativa mais recente de um prontuário.

        Args:
            prontuario (str): Prontuário do paciente.

        Returns:
            Optional[Dict[str, Any]]: Dados da cirurgia mapeados em dicionário, ou None.
        """
        query_text = get_sql_query('obter_cirurgia_aghu.sql')
        result = await self.session.execute(text(query_text), {"prontuario": prontuario})
        row = result.mappings().first()
        if not row:
            return None
        return dict(row)
