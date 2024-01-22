"""create users table

Revision ID: d9235ac4aefb
Revises: 8f15c6a0d6e7
Create Date: 2024-01-22 16:40:28.204022

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd9235ac4aefb'
down_revision: Union[str, None] = '8f15c6a0d6e7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',sa.Column('id',sa.Integer(),primary_key=True),
                            sa.Column('email',sa.String(),unique=True,nullable=False),
                            sa.Column('password',sa.String(),nullable=False),
                            sa.Column('created_at',sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'),nullable=False))
    


def downgrade() -> None:
    op.drop_table('users')
    
