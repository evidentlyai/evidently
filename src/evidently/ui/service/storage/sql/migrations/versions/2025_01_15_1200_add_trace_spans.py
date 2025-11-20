"""add trace spans

Revision ID: f1e2d3c4b5a6
Revises: a1b2c3d4e5f6
Create Date: 2025-01-15 12:00:00.000000

"""

from typing import Sequence
from typing import Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f1e2d3c4b5a6"
down_revision: Union[str, None] = "a1b2c3d4e5f6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "trace_spans",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("timestamp", sa.DateTime(), nullable=False),
        sa.Column("trace_id", sa.Uuid(), nullable=False),
        sa.Column("export_id", sa.Uuid(), nullable=False),
        sa.Column("trace_state", sa.String(), nullable=False),
        sa.Column("span_id", sa.String(), nullable=False),
        sa.Column("parent_span_id", sa.String(), nullable=True),
        sa.Column("span_name", sa.String(), nullable=False),
        sa.Column("span_kind", sa.String(), nullable=False),
        sa.Column("scope_name", sa.String(), nullable=False),
        sa.Column("service_name", sa.String(), nullable=False),
        sa.Column("resource_attributes", sa.JSON(), nullable=False),
        sa.Column("span_attributes", sa.JSON(), nullable=False),
        sa.Column("end_time", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("trace_spans_export_id_idx", "trace_spans", ["export_id"], unique=False)
    op.create_index("trace_spans_trace_id_idx", "trace_spans", ["trace_id"], unique=False)
    op.create_index("trace_spans_timestamp_idx", "trace_spans", ["timestamp"], unique=False)


def downgrade() -> None:
    op.drop_index("trace_spans_timestamp_idx", table_name="trace_spans")
    op.drop_index("trace_spans_trace_id_idx", table_name="trace_spans")
    op.drop_index("trace_spans_export_id_idx", table_name="trace_spans")
    op.drop_table("trace_spans")
