"""fixed users: added role

Revision ID: 7a091d745537
Revises: 4e4b6af75119
Create Date: 2024-12-10 23:36:41.166273

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7a091d745537'
down_revision: Union[str, None] = '4e4b6af75119'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('is_admin', sa.Boolean(), server_default=sa.text('false'), nullable=False), schema='flower_shop_schema')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'is_admin', schema='flower_shop_schema')
    # ### end Alembic commands ###