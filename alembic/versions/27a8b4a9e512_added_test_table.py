"""added test table

Revision ID: 27a8b4a9e512
Revises: None
Create Date: 2013-09-30 00:57:00.263221

"""

# revision identifiers, used by Alembic.
revision = '27a8b4a9e512'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
            'test_table',
            sa.Column('id', sa.Integer, primary_key=True)
    )
    


def downgrade():
    op.drop_table('test_table')
