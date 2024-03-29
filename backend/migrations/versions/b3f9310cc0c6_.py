"""empty message

Revision ID: b3f9310cc0c6
Revises: dde8d445bd8d
Create Date: 2020-11-07 14:27:29.139819

"""
from alembic import op
import sqlalchemy as sa
from passlib.hash import pbkdf2_sha256 as sha256
from uuid import uuid4
from flower.config import (
    ADMIN_DISPLAY_NAME, ADMIN_EMAIL, ADMIN_PASSWORD, ADMIN_USERNAME,
)

# revision identifiers, used by Alembic.
revision = 'b3f9310cc0c6'
down_revision = 'dde8d445bd8d'
branch_labels = None
depends_on = None


t_users = sa.Table(
    'users',
    sa.MetaData(),
    sa.Column('username', sa.String),
    sa.Column('password', sa.String),
    sa.Column('email', sa.String),
    sa.Column('display_name', sa.String),
    sa.Column('session', sa.String),
    sa.Column('deactivated', sa.Boolean),
    sa.Column('role_id', sa.Integer)
)


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    connection = op.get_bind()
    connection.execute(
        sa.insert(t_users).values({
            'username': ADMIN_USERNAME,
            'password': sha256.hash(ADMIN_PASSWORD),
            'email': ADMIN_EMAIL,
            'display_name': ADMIN_DISPLAY_NAME,
            'session': str(uuid4()),
            'deactivated': False,
            'role_id': 1,
        })
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    connection = op.get_bind()
    connection.execute(
        sa.delete(t_users).where(t_users.c.username == ADMIN_USERNAME)
    )
    # ### end Alembic commands ###
