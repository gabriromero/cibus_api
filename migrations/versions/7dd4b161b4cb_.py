"""empty message

Revision ID: 7dd4b161b4cb
Revises: a4f09bf1b7fa
Create Date: 2023-01-11 15:57:18.462293

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7dd4b161b4cb'
down_revision = 'a4f09bf1b7fa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('restaurants', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.String(length=80), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('restaurants', schema=None) as batch_op:
        batch_op.drop_column('name')

    # ### end Alembic commands ###
