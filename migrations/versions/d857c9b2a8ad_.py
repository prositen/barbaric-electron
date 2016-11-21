""" Creates user and role database tables. Adds the admin role.

Revision ID: d857c9b2a8ad
Revises: None
Create Date: 2016-11-04 15:22:11.475732

"""

# revision identifiers, used by Alembic.
from sqlalchemy import column
from sqlalchemy import table

revision = 'd857c9b2a8ad'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('authenticated', sa.Boolean(), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_table('roles_users',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'role_id')
    )
    data_upgrades()
    ### end Alembic commands ###


def data_upgrades():
    role_table = table('role',
                       column('id', sa.Integer()),
                       column('name', sa.String(length=80)),
                       column('description', sa.String(length=255))
                       )

    op.bulk_insert(role_table,
                   [
                       {'name': 'Admin',
                        'description': 'Admin capabilities'}
                   ])

def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('roles_users')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_table('role')
    ### end Alembic commands ###
