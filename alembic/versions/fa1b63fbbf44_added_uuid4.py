"""added vehicle enties view

Revision ID: fa1b63fbbf44
Revises: 8de7045f8c04
Create Date: 2021-03-03 09:46:02.637848

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fa1b63fbbf44'
down_revision = '8de7045f8c04'
branch_labels = None
depends_on = None


ddl = 'CREATE EXTENSION IF NOT EXISTS "uuid-ossp"'

drop_dll = 'DROP EXTENSION "ossp"'


def upgrade():
    op.execute(ddl)


def downgrade():
    op.execute(drop_dll)
