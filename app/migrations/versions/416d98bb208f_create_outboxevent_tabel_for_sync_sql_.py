"""create outboxevent tabel for sync sql with non sql

Revision ID: 416d98bb208f
Revises: cd3b3e1a2668
Create Date: 2025-08-09 00:06:53.557380

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '416d98bb208f'
down_revision: Union[str, None] = 'cd3b3e1a2668'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
