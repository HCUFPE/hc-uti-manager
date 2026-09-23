"""add_audit_logs_table

Revision ID: 79d49ce1ecad
Revises: 508c5cccfa30
Create Date: 2026-09-23 13:34:04.235319

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '79d49ce1ecad'
down_revision: Union[str, Sequence[str], None] = '508c5cccfa30'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('audit_logs',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('timestamp', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('categoria', sa.String(length=50), nullable=False),
    sa.Column('acao', sa.String(length=100), nullable=False),
    sa.Column('usuario_id', sa.String(length=100), nullable=True),
    sa.Column('detalhes', sa.Text(), nullable=True),
    sa.Column('estado_anterior', sa.Text(), nullable=True),
    sa.Column('estado_novo', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_audit_logs_acao'), 'audit_logs', ['acao'], unique=False)
    op.create_index(op.f('ix_audit_logs_categoria'), 'audit_logs', ['categoria'], unique=False)
    op.create_index(op.f('ix_audit_logs_timestamp'), 'audit_logs', ['timestamp'], unique=False)
    op.create_index(op.f('ix_audit_logs_usuario_id'), 'audit_logs', ['usuario_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_audit_logs_usuario_id'), table_name='audit_logs')
    op.drop_index(op.f('ix_audit_logs_timestamp'), table_name='audit_logs')
    op.drop_index(op.f('ix_audit_logs_categoria'), table_name='audit_logs')
    op.drop_index(op.f('ix_audit_logs_acao'), table_name='audit_logs')
    op.drop_table('audit_logs')
