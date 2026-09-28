"""add_ip_origem_to_audit_logs

Revision ID: e73de47db315
Revises: 79d49ce1ecad
Create Date: 2026-09-23 14:08:48.366271

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e73de47db315'
down_revision: Union[str, Sequence[str], None] = '79d49ce1ecad'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('audit_logs', sa.Column('ip_origem', sa.String(length=45), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('audit_logs', 'ip_origem')
