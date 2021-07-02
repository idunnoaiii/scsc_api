"""0701 associate Item - Category

Revision ID: 23bd44134aad
Revises: c13c5fbe5e8f
Create Date: 2021-07-01 20:43:43.584241

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '23bd44134aad'
down_revision = 'c13c5fbe5e8f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categoryitems',
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.Column('item_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
    sa.ForeignKeyConstraint(['item_id'], ['items.id'], )
    )
    op.drop_constraint('items_category_id_fkey', 'items', type_='foreignkey')
    op.drop_column('items', 'expired_date')
    op.drop_column('items', 'category_id')
    op.alter_column('orders', 'code', type_=sa.BIGINT(), existing_type=sa.INTEGER())
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('items', sa.Column('category_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('items', sa.Column('expired_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.create_foreign_key('items_category_id_fkey', 'items', 'categories', ['category_id'], ['id'])
    op.drop_table('categoryitems')
    op.alter_column('orders', 'code', type_=sa.INTEGER(), existing_type=sa.BIGINT())
    # ### end Alembic commands ###