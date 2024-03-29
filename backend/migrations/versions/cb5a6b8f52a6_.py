"""new permissions + alter column contract id

Revision ID: cb5a6b8f52a6
Revises: 03bb7ee4e504
Create Date: 2021-01-25 02:21:21.642580

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cb5a6b8f52a6'
down_revision = '03bb7ee4e504'
branch_labels = None
depends_on = None


t_permissions = sa.Table(
    'permissions',
    sa.MetaData(),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('app_name', sa.String(length=20), nullable=False),
    sa.Column('action', sa.String(length=20), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=False),
)


def upgrade():
    connection = op.get_bind()
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('purchases', 'contract_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
    connection.execute(
        sa.insert(t_permissions).values([
            {'app_name': 'purchases', 'action': 'update_status', 'role_id': 1},
            {'app_name': 'purchases', 'action': 'update_status', 'role_id': 2},
            {'app_name': 'purchases', 'action': 'update_status', 'role_id': 4},
        ])
    )

    connection.execute(
        sa.delete(t_permissions).where(
            (t_permissions.c.action == 'update')
            & (t_permissions.c.app_name == 'purchases')
        )
    )


def downgrade():
    connection = op.get_bind()
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('purchases', 'contract_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###

    connection.execute(
        sa.insert(t_permissions).values([
            {'app_name': 'purchases', 'action': 'update', 'role_id': 1},
            {'app_name': 'purchases', 'action': 'update', 'role_id': 2},
        ])
    )

    connection.execute(
        sa.delete(t_permissions).where(
            (t_permissions.c.action == 'update_status')
            & (t_permissions.c.app_name == 'purchases')
        )
    )

