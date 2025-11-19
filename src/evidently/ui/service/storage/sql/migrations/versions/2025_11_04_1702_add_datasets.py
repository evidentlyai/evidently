"""add datasets

Revision ID: a1b2c3d4e5f6
Revises: ea07771bba05
Create Date: 2025-11-04 17:02:00.000000

"""

from typing import Sequence
from typing import Union

# revision identifiers, used by Alembic.
revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, None] = "ea07771bba05"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Datasets table is now created in the initial migration
    # This migration is kept for migration history compatibility
    pass


def downgrade() -> None:
    # Datasets table is dropped in the initial migration downgrade
    pass
