"""add a content column

Revision ID: 8f15c6a0d6e7
Revises: 03484a8e95bc
Create Date: 2024-01-22 16:30:26.634179

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8f15c6a0d6e7'
down_revision: Union[str, None] = '03484a8e95bc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('contnet',sa.String(),nullable=False))
    


def downgrade() -> None:
    op.drop_column('posts','contnet')
    pass
