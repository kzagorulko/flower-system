"""added permissions

Revision ID: dde8d445bd8d
Revises: 6680bd9737cf
Create Date: 2020-11-04 15:57:18.773108

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dde8d445bd8d'
down_revision = '6680bd9737cf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    t_permissions = op.create_table(
        'permissions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('app_name', sa.String(length=20), nullable=False),
        sa.Column('action', sa.String(length=20), nullable=False),
        sa.Column('role_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(tuple(['role_id']), ['roles.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    t_roles = sa.Table(
        'roles',
        sa.MetaData(),
        sa.Column('id', sa.Integer),
        sa.Column('name', sa.String),
        sa.Column('display_name', sa.String)
    )

    connection = op.get_bind()

    connection.execute(
        sa.insert(t_roles).values([
            {
                'id': 2,
                'name': 'sales_department',
                'display_name': 'Отдел продаж',
            },
            {
                'id': 3,
                'name': 'law_department',
                'display_name': 'Юридический отдел'
            },
            {
                'id': 4,
                'name': 'logistics_department',
                'display_name': 'Отдел логистики'
            },
            {
                'id': 5,
                'name': 'branches',
                'display_name': 'Филиал'
            },
            {
                'id': 6,
                'name': 'demo',
                'display_name': 'Демо'
            },
        ])
    )

    connection.execute(
        sa.insert(t_permissions).values([
            # Поставки
            {'app_name': 'supplies', 'action': 'create', 'role_id': 1},
            {'app_name': 'supplies', 'action': 'create', 'role_id': 2},

            {'app_name': 'supplies', 'action': 'update', 'role_id': 1},
            {'app_name': 'supplies', 'action': 'update', 'role_id': 4},

            {'app_name': 'supplies', 'action': 'get', 'role_id': 1},
            {'app_name': 'supplies', 'action': 'get', 'role_id': 2},
            {'app_name': 'supplies', 'action': 'get', 'role_id': 4},
            {'app_name': 'supplies', 'action': 'get', 'role_id': 6},

            {'app_name': 'supplies', 'action': 'get_one', 'role_id': 1},
            {'app_name': 'supplies', 'action': 'get_one', 'role_id': 2},
            {'app_name': 'supplies', 'action': 'get_one', 'role_id': 4},
            {'app_name': 'supplies', 'action': 'get_one', 'role_id': 5},
            {'app_name': 'supplies', 'action': 'get_one', 'role_id': 6},

            # Филиалы
            {'app_name': 'branches', 'action': 'get', 'role_id': 1},
            {'app_name': 'branches', 'action': 'get', 'role_id': 2},
            {'app_name': 'branches', 'action': 'get', 'role_id': 3},
            {'app_name': 'branches', 'action': 'get', 'role_id': 4},
            {'app_name': 'branches', 'action': 'get', 'role_id': 6},

            {'app_name': 'branches', 'action': 'get_one', 'role_id': 1},
            {'app_name': 'branches', 'action': 'get_one', 'role_id': 2},
            {'app_name': 'branches', 'action': 'get_one', 'role_id': 3},
            {'app_name': 'branches', 'action': 'get_one', 'role_id': 4},
            {'app_name': 'branches', 'action': 'get_one', 'role_id': 5},
            {'app_name': 'branches', 'action': 'get_one', 'role_id': 6},

            {'app_name': 'branches', 'action': 'create', 'role_id': 1},

            {'app_name': 'branches', 'action': 'update', 'role_id': 1},

            # Заявки
            {'app_name': 'requests', 'action': 'get', 'role_id': 1},
            {'app_name': 'requests', 'action': 'get', 'role_id': 2},
            {'app_name': 'requests', 'action': 'get', 'role_id': 3},
            {'app_name': 'requests', 'action': 'get', 'role_id': 4},
            {'app_name': 'requests', 'action': 'get', 'role_id': 5},
            {'app_name': 'requests', 'action': 'get', 'role_id': 6},

            {'app_name': 'requests', 'action': 'create', 'role_id': 1},
            {'app_name': 'requests', 'action': 'create', 'role_id': 2},
            {'app_name': 'requests', 'action': 'create', 'role_id': 3},
            {'app_name': 'requests', 'action': 'create', 'role_id': 4},
            {'app_name': 'requests', 'action': 'create', 'role_id': 5},

            {'app_name': 'requests', 'action': 'update', 'role_id': 1},
            {'app_name': 'requests', 'action': 'update', 'role_id': 2},
            {'app_name': 'requests', 'action': 'update', 'role_id': 3},
            {'app_name': 'requests', 'action': 'update', 'role_id': 4},


            # Поставщики
            {'app_name': 'providers', 'action': 'get', 'role_id': 1},
            {'app_name': 'providers', 'action': 'get', 'role_id': 2},
            {'app_name': 'providers', 'action': 'get', 'role_id': 3},
            {'app_name': 'providers', 'action': 'get', 'role_id': 4},
            {'app_name': 'providers', 'action': 'get', 'role_id': 6},

            {'app_name': 'providers', 'action': 'create', 'role_id': 1},
            {'app_name': 'providers', 'action': 'create', 'role_id': 2},

            {'app_name': 'providers', 'action': 'update', 'role_id': 1},
            {'app_name': 'providers', 'action': 'update', 'role_id': 2},

            {'app_name': 'providers', 'action': 'update_status', 'role_id': 1},
            {'app_name': 'providers', 'action': 'update_status', 'role_id': 3},

            # Контракты
            {'app_name': 'contracts', 'action': 'get', 'role_id': 1},
            {'app_name': 'contracts', 'action': 'get', 'role_id': 2},
            {'app_name': 'contracts', 'action': 'get', 'role_id': 3},
            {'app_name': 'contracts', 'action': 'get', 'role_id': 6},

            {'app_name': 'contracts', 'action': 'create', 'role_id': 1},
            {'app_name': 'contracts', 'action': 'create', 'role_id': 2},

            # Продажи
            {'app_name': 'sales', 'action': 'get', 'role_id': 1},
            {'app_name': 'sales', 'action': 'get', 'role_id': 2},
            {'app_name': 'sales', 'action': 'get', 'role_id': 5},
            {'app_name': 'sales', 'action': 'get', 'role_id': 6},

            {'app_name': 'sales', 'action': 'create', 'role_id': 1},
            {'app_name': 'sales', 'action': 'create', 'role_id': 5},

            # Склады
            {'app_name': 'warehouses', 'action': 'get', 'role_id': 1},
            {'app_name': 'warehouses', 'action': 'get', 'role_id': 2},
            {'app_name': 'warehouses', 'action': 'get', 'role_id': 4},
            {'app_name': 'warehouses', 'action': 'get', 'role_id': 6},

            {'app_name': 'warehouses', 'action': 'update', 'role_id': 1},
            {'app_name': 'warehouses', 'action': 'update', 'role_id': 4},

            {'app_name': 'warehouses', 'action': 'create', 'role_id': 1},

            # Закупки
            {'app_name': 'purchases', 'action': 'create', 'role_id': 1},
            {'app_name': 'purchases', 'action': 'create', 'role_id': 2},

            {'app_name': 'purchases', 'action': 'get', 'role_id': 1},
            {'app_name': 'purchases', 'action': 'get', 'role_id': 2},
            {'app_name': 'purchases', 'action': 'get', 'role_id': 4},
            {'app_name': 'purchases', 'action': 'get', 'role_id': 6},

            {'app_name': 'purchases', 'action': 'update', 'role_id': 1},
            {'app_name': 'purchases', 'action': 'update', 'role_id': 2},

            {
                'app_name': 'purchases',
                'action': 'update_warehouse',
                'role_id': 1
            },
            {
                'app_name': 'purchases',
                'action': 'update_warehouse',
                'role_id': 4
            },

            # Продукты
            {'app_name': 'products', 'action': 'get', 'role_id': 1},
            {'app_name': 'products', 'action': 'get', 'role_id': 2},
            {'app_name': 'products', 'action': 'get', 'role_id': 4},
            {'app_name': 'products', 'action': 'get', 'role_id': 5},
            {'app_name': 'products', 'action': 'get', 'role_id': 6},

            {'app_name': 'products', 'action': 'create', 'role_id': 1},
            {'app_name': 'products', 'action': 'create', 'role_id': 2},

            {'app_name': 'products', 'action': 'update', 'role_id': 1},
            {'app_name': 'products', 'action': 'update', 'role_id': 2},

            # Пользователи
            {'app_name': 'users', 'action': 'get', 'role_id': 1},
            {'app_name': 'users', 'action': 'get', 'role_id': 2},
            {'app_name': 'users', 'action': 'get', 'role_id': 3},
            {'app_name': 'users', 'action': 'get', 'role_id': 4},
            {'app_name': 'users', 'action': 'get', 'role_id': 5},
            {'app_name': 'users', 'action': 'get', 'role_id': 6},

            {'app_name': 'users', 'action': 'create', 'role_id': 1},

            {'app_name': 'users', 'action': 'update', 'role_id': 1},
        ])
    )

    op.alter_column(
        'users', 'session',
        existing_type=sa.VARCHAR(length=36),
        nullable=False
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        'users', 'session',
        existing_type=sa.VARCHAR(length=36),
        nullable=True
    )
    op.drop_table('permissions')

    t_users = sa.Table(
        'users',
        sa.MetaData(),
        sa.Column('id', sa.Integer),
        sa.Column('username', sa.String),
        sa.Column('deactivated', sa.Boolean),
        sa.Column('display_name', sa.String),
        sa.Column('email', sa.String),
        sa.Column('session', sa.String),
        sa.Column('role_id', sa.Integer)
    )

    t_roles = sa.Table(
        'roles',
        sa.MetaData(),
        sa.Column('id', sa.Integer),
        sa.Column('name', sa.String),
        sa.Column('display_name', sa.String)
    )

    connection = op.get_bind()

    connection.execute(
        sa.update(t_users).values(role_id=1)
    )

    connection.execute(
        sa.delete(t_roles).where(t_roles.c.id != 1)
    )
    # ### end Alembic commands ###
