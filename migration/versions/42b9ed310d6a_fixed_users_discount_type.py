"""fixed users.discount type

Revision ID: 42b9ed310d6a
Revises: d33c3bdbc50c
Create Date: 2024-11-24 01:20:00.815559

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from java_luchshe.project.core.config import settings

# revision identifiers, used by Alembic.
revision: str = '42b9ed310d6a'
down_revision: Union[str, None] = 'd33c3bdbc50c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'discount',
               existing_type=sa.VARCHAR(length=255),
               type_=sa.Integer(),
               existing_nullable=True,
               postgresql_using='discount::integer',
               schema=settings.POSTGRES_SCHEMA)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'discount',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(length=255),
               existing_nullable=True,
               schema=settings.POSTGRES_SCHEMA)
    # ### end Alembic commands ###