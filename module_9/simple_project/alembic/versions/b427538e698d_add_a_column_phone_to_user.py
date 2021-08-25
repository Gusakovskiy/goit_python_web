"""Add a column phone to user

Revision ID: b427538e698d
Revises: 26979f2a8154
Create Date: 2021-08-25 13:49:46.518274+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b427538e698d'
down_revision = '26979f2a8154'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('app_user', sa.Column('phone', sa.String(50)))


def downgrade():
    op.drop_column('app_user', 'phone')
