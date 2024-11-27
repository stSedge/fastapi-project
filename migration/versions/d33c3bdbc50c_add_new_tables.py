"""add new tables

Revision ID: d33c3bdbc50c
Revises: 
Create Date: 2024-11-16 14:44:04.685662

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from java_luchshe.project.core.config import settings


# revision identifiers, used by Alembic.
revision: str = 'd33c3bdbc50c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sellers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String().with_variant(sa.String(length=255), 'postgresql'), nullable=False),
    sa.Column('age', sa.Integer(), nullable=False),
    sa.Column('gender', sa.String().with_variant(sa.String(length=255), 'postgresql'), nullable=False),
    sa.Column('data_start', sa.Date(), nullable=False),
    sa.Column('data_end', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    schema=settings.POSTGRES_SCHEMA
    )
    op.create_table('type_of_product',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String().with_variant(sa.String(length=255), 'postgresql'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    schema=settings.POSTGRES_SCHEMA
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String().with_variant(sa.String(length=255), 'postgresql'), nullable=False),
    sa.Column('age', sa.Integer(), nullable=False),
    sa.Column('gender', sa.String().with_variant(sa.String(length=255), 'postgresql'), nullable=False),
    sa.Column('total_sum', sa.Integer(), nullable=False),
    sa.Column('discount', sa.String().with_variant(sa.String(length=255), 'postgresql'), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    schema=settings.POSTGRES_SCHEMA
    )
    op.create_table('additional_products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String().with_variant(sa.String(length=255), 'postgresql'), nullable=False),
    sa.Column('id_type', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_type'], ['flower_shop_schema.type_of_product.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    schema=settings.POSTGRES_SCHEMA
    )
    op.create_table('bouquets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String().with_variant(sa.String(length=255), 'postgresql'), nullable=False),
    sa.Column('id_type', sa.Integer(), nullable=False),
    sa.Column('size', sa.String().with_variant(sa.String(length=255), 'postgresql'), nullable=True),
    sa.ForeignKeyConstraint(['id_type'], ['flower_shop_schema.type_of_product.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    schema=settings.POSTGRES_SCHEMA
    )
    op.create_table('flowers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String().with_variant(sa.String(length=255), 'postgresql'), nullable=False),
    sa.Column('id_type', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_type'], ['flower_shop_schema.type_of_product.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    schema=settings.POSTGRES_SCHEMA
    )
    op.create_table('supply',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_type', sa.Integer(), nullable=False),
    sa.Column('id_product', sa.Integer(), nullable=False),
    sa.Column('count', sa.Integer(), nullable=False),
    sa.Column('cost', sa.Integer(), nullable=False),
    sa.Column('id_seller', sa.Integer(), nullable=False),
    sa.Column('data', sa.Date(), nullable=False),
    sa.ForeignKeyConstraint(['id_seller'], ['flower_shop_schema.sellers.id'], ),
    sa.ForeignKeyConstraint(['id_type'], ['flower_shop_schema.type_of_product.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    schema=settings.POSTGRES_SCHEMA
    )
    op.create_table('compound_bouquet',
    sa.Column('id_bouquet', sa.Integer(), nullable=False),
    sa.Column('id_flower', sa.Integer(), nullable=False),
    sa.Column('count', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_bouquet'], ['flower_shop_schema.bouquets.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['id_flower'], ['flower_shop_schema.flowers.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id_bouquet', 'id_flower'),
    schema=settings.POSTGRES_SCHEMA
    )
    op.create_table('selling',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_supply', sa.Integer(), nullable=False),
    sa.Column('id_user', sa.Integer(), nullable=False),
    sa.Column('count', sa.Integer(), nullable=False),
    sa.Column('cost', sa.Integer(), nullable=False),
    sa.Column('id_seller', sa.Integer(), nullable=False),
    sa.Column('discount', sa.Integer(), nullable=False),
    sa.Column('final_cost', sa.Integer(), nullable=False),
    sa.Column('data', sa.Date(), nullable=False),
    sa.ForeignKeyConstraint(['id_seller'], ['flower_shop_schema.sellers.id'], ),
    sa.ForeignKeyConstraint(['id_supply'], ['flower_shop_schema.supply.id'], ),
    sa.ForeignKeyConstraint(['id_user'], ['flower_shop_schema.users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema=settings.POSTGRES_SCHEMA
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('selling', schema=settings.POSTGRES_SCHEMA)
    op.drop_table('compound_bouquet', schema=settings.POSTGRES_SCHEMA)
    op.drop_table('supply', schema=settings.POSTGRES_SCHEMA)
    op.drop_table('flowers', schema=settings.POSTGRES_SCHEMA)
    op.drop_table('bouquets', schema=settings.POSTGRES_SCHEMA)
    op.drop_table('additional_products', schema=settings.POSTGRES_SCHEMA)
    op.drop_table('users', schema=settings.POSTGRES_SCHEMA)
    op.drop_table('type_of_product', schema=settings.POSTGRES_SCHEMA)
    op.drop_table('sellers', schema=settings.POSTGRES_SCHEMA)
    # ### end Alembic commands ###
