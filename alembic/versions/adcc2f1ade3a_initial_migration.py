"""Initial migration

Revision ID: adcc2f1ade3a
Revises: db0a1b94f81b
Create Date: 2024-10-11 19:53:33.121883

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'adcc2f1ade3a'
down_revision: Union[str, None] = 'db0a1b94f81b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('click_info',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('product_id', sa.UUID(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('click_info')
    # ### end Alembic commands ###
