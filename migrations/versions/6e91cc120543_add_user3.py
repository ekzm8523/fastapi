"""add user3

Revision ID: 6e91cc120543
Revises: dd035322cf69
Create Date: 2021-10-08 16:17:10.930354

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '6e91cc120543'
down_revision = 'dd035322cf69'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('create_dt', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('update_dt', postgresql.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('email', sa.String(length=128), nullable=True),
    sa.Column('password', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('uuid')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###