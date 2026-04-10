"""add last few columns to post table

Revision ID: fe7e5c9f17d6
Revises: 1c2b5737934d
Create Date: 2026-04-10 20:53:18.510849

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fe7e5c9f17d6'
down_revision: Union[str, Sequence[str], None] = '1c2b5737934d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='True'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, 
                                     server_default=sa.text('NOW()')))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')

    pass
