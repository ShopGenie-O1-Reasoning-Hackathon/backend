"""Initial migration

Revision ID: 3b8d022fe0d7
Revises: cf5f82d15ccc
Create Date: 2024-10-11 16:10:18.738623

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3b8d022fe0d7'
down_revision: Union[str, None] = 'cf5f82d15ccc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
