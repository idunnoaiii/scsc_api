"""0626 add tables orderitems

Revision ID: 21bb650ab650
Revises: 6844f63c90e4
Create Date: 2021-06-26 23:12:05.943484

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '21bb650ab650'
down_revision = '6844f63c90e4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('orderitems',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('created_date', sa.DateTime(), nullable=True),
    sa.Column('updated_date', sa.DateTime(), nullable=True),
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.Column('item_id', sa.Integer(), nullable=True),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('item_name', sa.String(length=100), nullable=True),
    sa.ForeignKeyConstraint(['item_id'], ['items.id'], ),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_orderitems_id'), 'orderitems', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_orderitems_id'), table_name='orderitems')
    op.drop_table('orderitems')
    # ### end Alembic commands ###