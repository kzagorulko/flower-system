"""added branches

Revision ID: 7292deb23125
Revises: b1a0d6cd7fa7
Create Date: 2020-11-08 00:27:30.440779

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '7292deb23125'
down_revision = 'b1a0d6cd7fa7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    t_branches = op.create_table(
        'branches',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('address', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('address')
    )
    op.create_table(
        'user_x_branch',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('branch_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(tuple(['branch_id']), ['branches.id'], ),
        sa.ForeignKeyConstraint(tuple(['user_id']), ['users.id'], ),
    )
    # ### end Alembic commands ###

    connection = op.get_bind()

    connection.execute(
        sa.insert(t_branches).values([
            {
                'id': 1,
                'address': 'г. Москва, ул. Пушкина, д. 30'
            },
            {
                'id': 2,
                'address': 'г. Москва, ул. Молодогвардейская, д. 61, стр.16'
            },
        ]),
    )


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_x_branch')
    op.drop_table('branches')
    # ### end Alembic commands ###
