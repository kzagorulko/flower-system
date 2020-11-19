"""added request and request categories tables

Revision ID: f7f61b0fadff
Revises: 14af6017bb46
Create Date: 2020-11-07 21:34:58.470451

"""
from alembic import op
import sqlalchemy as sa
import gino.dialects.asyncpg


# revision identifiers, used by Alembic.
revision = 'f7f61b0fadff'
down_revision = '14af6017bb46'
branch_labels = None
depends_on = None


t_permissions = sa.Table(
    'permissions',
    sa.MetaData(),
    sa.Column('id', sa.Integer),
    sa.Column('app_name', sa.String),
    sa.Column('action', sa.String),
    sa.Column('role_id', sa.Integer)
)

request_status_type = gino.dialects.asyncpg.AsyncEnum(
    'NEW', 'IN_PROGRESS', 'CANCELLED', 'DONE', name='requeststatus'
)


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    t_request_categories = op.create_table(
        'request_categories',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'requests',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('description', sa.String(length=400), nullable=False),
        sa.Column('created', sa.DateTime(timezone=True), nullable=False),
        sa.Column('creator_id', sa.Integer(), nullable=False),
        sa.Column('department_id', sa.Integer(), nullable=False),
        sa.Column('category_id', sa.Integer(), nullable=False),
        sa.Column('executor_id', sa.Integer(), nullable=True),
        sa.Column('status', request_status_type, nullable=False),
        sa.ForeignKeyConstraint(
            tuple(['category_id']), ['request_categories.id'],
        ),
        sa.ForeignKeyConstraint(tuple(['creator_id']), ['users.id'], ),
        sa.ForeignKeyConstraint(tuple(['department_id']), ['roles.id'], ),
        sa.ForeignKeyConstraint(tuple(['executor_id']), ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    connection = op.get_bind()

    connection.execute(
        sa.insert(t_permissions).values([
            {
                'app_name': 'requests',
                'action': 'create_category',
                'role_id': 1
            },
            {
                'app_name': 'requests',
                'action': 'update_category',
                'role_id': 1
            },
        ])
    )

    connection.execute(
        sa.insert(t_request_categories).values([
            {
                'name': 'Поломка оборудования'
            },
            {
                'name': 'Корректировка данных'
            },
            {
                'name': 'Изменение количества товара'
            },
            {
                'name': 'Смена склада для закупки'
            },
            {
                'name': 'Смена поставщика'
            },
            {
                'name': 'Проверка поставщика'
            },
            {
                'name': 'Судебное разбирательство'
            },
            {
                'name': 'Смена даты поставок'
            },
            {
                'name': 'Техническая поддержка'
            },
        ])
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('requests')
    op.drop_table('request_categories')
    connection = op.get_bind()

    connection.execute(
            sa.delete(t_permissions).where(
                (t_permissions.c.app_name == 'request')
                & (
                    (t_permissions.c.action == 'create_category')
                    | (t_permissions.c.action == 'update_category')
                )
            )
        )
    request_status_type.drop(op.get_bind(), checkfirst=True)
    # ### end Alembic commands ###
