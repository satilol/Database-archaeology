"""Add index for search

Revision ID: 8d89e16db042
Revises: 377e9e5fd830
Create Date: 2025-12-30 19:19:09.026865

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8d89e16db042'
down_revision: Union[str, Sequence[str], None] = '377e9e5fd830'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_index('idx_artifact_name', 'artifacts', ['name'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index('idx_artifact_name', table_name='artifacts')