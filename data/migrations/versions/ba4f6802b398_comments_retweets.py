"""comments_retweets

Revision ID: ba4f6802b398
Revises: 604fefcb31bb
Create Date: 2022-05-05 15:13:25.479066

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ba4f6802b398'
down_revision = '604fefcb31bb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Posts', sa.Column('retweets', sa.Integer(), nullable=False, server_default='0'))
    op.add_column('Posts', sa.Column('comments', sa.Integer(), nullable=False, server_default='0'))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Posts', 'comments')
    op.drop_column('Posts', 'retweets')
    # ### end Alembic commands ###
