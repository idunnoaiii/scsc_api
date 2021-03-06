"""0724 update customer table

Revision ID: e4f2f8d935c2
Revises: 7de557f6cf10
Create Date: 2021-07-24 20:57:06.517828

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e4f2f8d935c2'
down_revision = '7de557f6cf10'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('customers', sa.Column('contact', sa.String(), nullable=True))
    op.add_column('customers', sa.Column('address', sa.String(), nullable=True))
    op.alter_column('customers', 'name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.drop_index('ix_customers_phone', table_name='customers')
    op.create_index(op.f('ix_customers_contact'), 'customers', ['contact'], unique=True)
    op.drop_column('customers', 'phone')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('customers', sa.Column('phone', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_index(op.f('ix_customers_contact'), table_name='customers')
    op.create_index('ix_customers_phone', 'customers', ['phone'], unique=False)
    op.alter_column('customers', 'name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_column('customers', 'address')
    op.drop_column('customers', 'contact')
    # ### end Alembic commands ###
