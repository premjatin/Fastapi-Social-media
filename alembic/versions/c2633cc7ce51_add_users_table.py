"""add users table

Revision ID: c2633cc7ce51
Revises: 5b753b00fd5b
Create Date: 2025-10-24 12:15:56.469319

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c2633cc7ce51'
down_revision: Union[str, Sequence[str], None] = '5b753b00fd5b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('email', sa.String, nullable=False, unique=True),
        sa.Column('password', sa.String, nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('NOW()'), nullable=False),
    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
