"""added function table

Revision ID: 6353a7ed8fc1
Revises: f76766a5e0e1
Create Date: 2021-03-02 22:10:45.949540

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '6353a7ed8fc1'
down_revision = 'f76766a5e0e1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('base_function',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('modified_at', sa.DateTime(), nullable=True),
    sa.Column('deleted', sa.Boolean(), nullable=True),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_base_function'))
    )
    op.create_index(op.f('ix_base_function_id'), 'base_function', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_base_function_id'), table_name='base_function')
    op.drop_table('base_function')
    # ### end Alembic commands ###
