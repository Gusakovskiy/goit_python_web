"""create account table

Revision ID: 26979f2a8154
Revises: 
Create Date: 2021-08-25 13:43:56.270385+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '26979f2a8154'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'app_user',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('first_name', sa.Unicode(50)),
        sa.Column('last_name', sa.Unicode(50)),
        sa.Column('address', sa.Unicode(200)),
        sa.Column('email', sa.String(50), nullable=False),
    )


def downgrade():
    op.drop_table('app_user')
