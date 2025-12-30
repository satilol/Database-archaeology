"""Add GIN index for JSON search

Revision ID: 0bbabb964180
Revises: 8d89e16db042
Create Date: 2025-12-30 19:42:02.811438

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0bbabb964180'
down_revision: Union[str, Sequence[str], None] = '8d89e16db042'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")
    op.execute(
        "CREATE INDEX idx_findings_json_gin ON findings USING gin (extra_data);"
    )


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS idx_findings_json_gin;")
