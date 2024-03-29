"""added password and identify columns

Revision ID: 498f307695d6
Revises: 4cc6a0c21606
Create Date: 2020-10-28 14:00:10.327966

"""
from uuid import uuid4
from alembic import op
import sqlalchemy as sa
from passlib.hash import pbkdf2_sha256 as sha256


# revision identifiers, used by Alembic.
revision = '498f307695d6'
down_revision = '4cc6a0c21606'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        'users', sa.Column('password', sa.String(length=120), nullable=True)
    )

    t_users = sa.Table(
        'users',
        sa.MetaData(),
        sa.Column('id', sa.Integer),
        sa.Column('identity', sa.String),
        sa.Column('password', sa.String)
    )

    connection = op.get_bind()
    connection.execute(
        sa.update(t_users).values(
            password=sha256.hash('123456')
        )
    )
    op.alter_column('users', 'password', nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'password')
    # ### end Alembic commands ###
