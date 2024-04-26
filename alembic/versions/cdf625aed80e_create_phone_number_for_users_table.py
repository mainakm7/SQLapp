"""create phone-number for users table

Revision ID: cdf625aed80e
Revises: 
Create Date: 2024-04-26 17:02:29.187919

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cdf625aed80e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("phone_number",sa.String(20), nullable=True))


def downgrade() -> None:
    op.drop_column("users", "phone_number")
