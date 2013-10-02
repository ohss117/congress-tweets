"""add a column

Revision ID: 46ff4b3fe2c7
Revises: 27a8b4a9e512
Create Date: 2013-09-30 01:03:39.520084

"""

# revision identifiers, used by Alembic.
revision = '46ff4b3fe2c7'
down_revision = '27a8b4a9e512'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('test_table', sa.Column('my_column', sa.String))



def downgrade():
    op.drop_column('test_table', 'my_column')
    
