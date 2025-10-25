"""add foreign key

Revision ID: 384b7892a6e7
Revises: c2633cc7ce51
Create Date: 2025-10-25 11:47:19.162743

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '384b7892a6e7'
down_revision: Union[str, Sequence[str], None] = 'c2633cc7ce51'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer, nullable=False))
    op.create_foreign_key('posts_owner_id_fkey',source_table= 'posts',referent_table= 'users',local_cols= ['owner_id'],remote_cols= ['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('posts_owner_id_fkey', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
