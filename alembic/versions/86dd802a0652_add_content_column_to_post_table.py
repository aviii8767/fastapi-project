"""add content column to post table

Revision ID: 86dd802a0652
Revises: 6e4665701017
Create Date: 2026-04-10 17:27:49.723867

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '86dd802a0652'
down_revision: Union[str, Sequence[str], None] = '6e4665701017'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'content')
    pass
