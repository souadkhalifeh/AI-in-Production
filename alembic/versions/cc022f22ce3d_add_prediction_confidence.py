"""add prediction confidence

Revision ID: cc022f22ce3d
Revises: 6439abf0b4d5
Create Date: 2026-10-14 16:38:10.710203

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cc022f22ce3d'
down_revision: Union[str, Sequence[str], None] = '6439abf0b4d5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('predictions', sa.Column('confidence', sa.Float(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('predictions', 'confidence')
