"""0724 update code order

Revision ID: 02605d95aff1
Revises: b00d57006dac
Create Date: 2021-07-25 09:40:38.076186

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '02605d95aff1'
down_revision = 'b00d57006dac'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('orders', 'code', type_=sa.VARCHAR(), existing_type=sa.BIGINT())
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('orders', 'code', type_=sa.BIGINT(), existing_type=sa.VARCHAR())
    # ### end Alembic commands ###