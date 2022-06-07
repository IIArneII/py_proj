"""change_column_name

Revision ID: 82b94fcac6e6
Revises: b249e061b3bb
Create Date: 2022-05-16 12:01:28.008561

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '82b94fcac6e6'
down_revision = 'b249e061b3bb'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('Posts', 'likes', new_column_name='likes_count')
    op.alter_column('Posts', 'retweets', new_column_name='retweets_count')
    op.alter_column('Posts', 'comments', new_column_name='comments_count')


def downgrade():
    op.alter_column('Posts', 'likes_count', new_column_name='likes')
    op.alter_column('Posts', 'retweets_count', new_column_name='retweets')
    op.alter_column('Posts', 'comments_count', new_column_name='comments')
