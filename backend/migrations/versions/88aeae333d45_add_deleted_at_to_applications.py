"""add deleted_at to applications

Revision ID: 88aeae333d45
Revises: 430eb0f1aecc
Create Date: 2026-06-26 00:16:01.972049

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '88aeae333d45'
down_revision: Union[str, Sequence[str], None] = '430eb0f1aecc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('applications', sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    op.add_column('applications', sa.Column('deleted_at', sa.DateTime(), nullable=True))


def downgrade() -> None:
    op.drop_column('applications', 'deleted_at')
    op.drop_column('applications', 'created_at')
