"""0721 add column to user table

Revision ID: e3d49543078d
Revises: 9fcad287e71a
Create Date: 2021-07-22 09:07:05.926315

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e3d49543078d'
down_revision = '9fcad287e71a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('adddress', sa.String(), nullable=True))
    op.add_column('users', sa.Column('contact', sa.String(), nullable=True))
    op.add_column('users', sa.Column('gender', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'gender')
    op.drop_column('users', 'contact')
    op.drop_column('users', 'adddress')
    # ### end Alembic commands ###
