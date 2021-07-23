"""0721 alter column name adddress -> address table users

Revision ID: f2d453484ad0
Revises: e3d49543078d
Create Date: 2021-07-22 13:32:44.862544

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f2d453484ad0'
down_revision = 'e3d49543078d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('address', sa.String(), nullable=True))
    op.drop_column('users', 'adddress')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('adddress', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('users', 'address')
    # ### end Alembic commands ###
