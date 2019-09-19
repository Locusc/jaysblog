"""empty message

Revision ID: 6b1a97070f70
Revises: 
Create Date: 2019-09-19 09:05:09.501372

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6b1a97070f70'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('b_users', sa.Column('create_time', sa.DateTime(), nullable=True))
    op.add_column('b_users', sa.Column('update_time', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('b_users', 'update_time')
    op.drop_column('b_users', 'create_time')
    # ### end Alembic commands ###