"""add_passagem_caso_column

Revision ID: 508c5cccfa30
Revises: e5cff95f7faa
Create Date: 2026-08-17 13:45:21.661974

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
"""add_passagem_caso_column

Revision ID: 508c5cccfa30
Revises: e5cff95f7faa
Create Date: 2026-08-17 13:45:21.661974

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '508c5cccfa30'
down_revision: Union[str, Sequence[str], None] = 'e5cff95f7faa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('solicitacoes_leito', sa.Column('passagem_caso', sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('solicitacoes_leito', 'passagem_caso')
