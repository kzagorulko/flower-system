"""Warehouses, Purchases, Supplies

Revision ID: e7136da05c80
Revises: f7f61b0fadff
Create Date: 2020-11-25 23:55:24.460135

"""
from pytz import utc
from alembic import op
from datetime import datetime
import sqlalchemy as sa
import gino.dialects.asyncpg


# revision identifiers, used by Alembic.
revision = 'e7136da05c80'
down_revision = '182718a0a9ae'
branch_labels = None
depends_on = None

purchase_status_type = gino.dialects.asyncpg.AsyncEnum(
    'NEW', 'IN_PROGRESS', 'CANCELLED', 'DONE', name='purchasestatus'
)

supply_status_type = gino.dialects.asyncpg.AsyncEnum(
    'NEW', 'IN_PROGRESS', 'CANCELLED', 'DONE', name='purchasestatus'
)


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    t_warehouses = op.create_table('warehouses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('address', sa.String(length=100), nullable=False),
    sa.Column('max_value', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('address')
    )
    t_product_in_warehouses = op.create_table('product_x_warehouse',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('value', sa.Float(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('warehouse_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(tuple(['product_id']), ['products.id'], ),
    sa.ForeignKeyConstraint(tuple(['warehouse_id']), ['warehouses.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    t_purchases = op.create_table('purchases',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('address', sa.String(100), nullable=False),
    sa.Column('value', sa.Float(), nullable=False),
    sa.Column('status', purchase_status_type, nullable=False),
    sa.Column('date', sa.DateTime(timezone=True), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.Column('warehouse_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(tuple(['product_id']), ['products.id'], ),
    sa.ForeignKeyConstraint(tuple(['warehouse_id']), ['warehouses.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    t_supplies = op.create_table('supplies',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('value', sa.Float(), nullable=False),
    sa.Column('status', supply_status_type, nullable=False),
    sa.Column('date', sa.DateTime(timezone=True), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.Column('warehouse_id', sa.Integer(), nullable=True),
    sa.Column('branch_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(tuple(['branch_id']), ['branches.id'], ),
    sa.ForeignKeyConstraint(tuple(['product_id']), ['products.id'], ),
    sa.ForeignKeyConstraint(tuple(['warehouse_id']), ['warehouses.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###

    connection = op.get_bind()

    connection.execute(
        sa.insert(t_warehouses).values([{
           'id': 1,
           'address': 'г. Москва, ул. Пушкина, д. 30',
           'max_value': 567
        }])
    )
    connection.execute(
        sa.insert(t_product_in_warehouses).values([{
            'id': 1,
            'product_id': 1,
            'warehouse_id': 1,
            'value': 300
        }])
    )
    connection.execute(
        sa.insert(t_purchases).values([{
            'id': 1,
            'product_id': 1,
            'warehouse_id': 1,
            'status': 'NEW',
            'value': 100,
            'address': 'м. Сокольники',
            'date': datetime.now().astimezone(utc)
        }])
    )
    connection.execute(
        sa.insert(t_supplies).values([{
            'id': 1,
            'product_id': 1,
            'warehouse_id': 1,
            'branch_id': 1,
            'value': 100,
            'status': 'NEW',
            'date': datetime.now().astimezone(utc)
        }])
    )


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('supplies')
    op.drop_table('purchases')
    op.drop_table('product_x_warehouse')
    op.drop_table('warehouses')

    # ### end Alembic commands ###

    purchase_status_type.drop(op.get_bind(), checkfirst=True)
    supply_status_type.drop(op.get_bind(), checkfirst=True)
