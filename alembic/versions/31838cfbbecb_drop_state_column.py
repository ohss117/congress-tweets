"""drop state column

Revision ID: 31838cfbbecb
Revises: 15b681f10782
Create Date: 2013-10-17 07:26:51.255352

"""

# revision identifiers, used by Alembic.
revision = '31838cfbbecb'
down_revision = '15b681f10782'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_column('congressmember', 'state')


def downgrade():
    op.add_column('congressmember', sa.Column('state', sa.String(length=2), nullable=True))

