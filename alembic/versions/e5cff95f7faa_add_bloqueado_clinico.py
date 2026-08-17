"""add_bloqueado_clinico

Revision ID: e5cff95f7faa
Revises: 1c7debc81e99
Create Date: 2026-08-14 15:37:32.815653

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e5cff95f7faa'
down_revision: Union[str, Sequence[str], None] = '1c7debc81e99'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Adiciona a coluna bloqueado_clinico com valor padrão False
    # No SQLite, para colunas NOT NULL, precisamos fornecer um server_default temporário
    # ou adicioná-la com nullable=True e depois alterar, mas adicionar como BOOLEAN nullable=False
    # com server_default=sa.text('0') é a forma mais segura.
    op.add_column('leito_estados', sa.Column('bloqueado_clinico', sa.Boolean(), nullable=False, server_default=sa.text('0')))


def downgrade() -> None:
    op.drop_column('leito_estados', 'bloqueado_clinico')
