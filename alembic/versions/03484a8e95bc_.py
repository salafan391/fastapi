"""empty message

Revision ID: 03484a8e95bc
Revises: 
Create Date: 2024-01-21 17:28:06.786429

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '03484a8e95bc'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts',
                    sa.Column('id',sa.Integer(),primary_key=True),
                    sa.Column('title',sa.String(),nullable=False),)


def downgrade() -> None:
    op.drop_table('posts')
