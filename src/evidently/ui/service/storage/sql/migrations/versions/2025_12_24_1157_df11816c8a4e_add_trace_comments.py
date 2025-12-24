"""add trace comments

Revision ID: df11816c8a4e
Revises: a7b8c9d0e1f2
Create Date: 2025-12-24 11:57:48.245600

"""

from typing import Sequence
from typing import Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "df11816c8a4e"
down_revision: Union[str, None] = "a7b8c9d0e1f2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("datasets", sa.Column("human_feedback_custom_shortcut_labels", sa.JSON(), nullable=True))


def downgrade() -> None:
    op.drop_column("datasets", "human_feedback_custom_shortcut_labels")
