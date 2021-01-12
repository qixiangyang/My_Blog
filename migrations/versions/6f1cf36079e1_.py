"""empty message

Revision ID: 6f1cf36079e1
Revises: 
Create Date: 2021-01-12 11:55:29.448968

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6f1cf36079e1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('access_log',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('route', sa.String(length=20), nullable=True),
    sa.Column('time', sa.TIMESTAMP(), nullable=True),
    sa.Column('ip_address', sa.String(length=20), nullable=True),
    sa.Column('cookie', sa.TEXT, nullable=True),
    sa.Column('user_agent', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('article',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=64), nullable=True),
    sa.Column('text', sa.Text(), nullable=True),
    sa.Column('text_pre', sa.String(length=500), nullable=True),
    sa.Column('author', sa.String(length=20), nullable=True),
    sa.Column('create_time', sa.TIMESTAMP(), nullable=True),
    sa.Column('update_time', sa.TIMESTAMP(), nullable=True),
    sa.Column('other_info', sa.String(length=100), nullable=True),
    sa.Column('status', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    op.create_table('pynews',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=200), nullable=True),
    sa.Column('text', sa.Text(), nullable=True),
    sa.Column('preview', sa.Text(), nullable=True),
    sa.Column('author', sa.String(length=50), nullable=True),
    sa.Column('category', sa.String(length=100), nullable=True),
    sa.Column('tags', sa.String(length=200), nullable=True),
    sa.Column('read_count', sa.Integer(), nullable=True),
    sa.Column('comment_count', sa.Integer(), nullable=True),
    sa.Column('pub_time', sa.TIMESTAMP(), nullable=True),
    sa.Column('url', sa.String(length=280), nullable=True),
    sa.Column('other_info', sa.String(length=170), nullable=True),
    sa.Column('blog_name', sa.String(length=160), nullable=True),
    sa.Column('line', sa.String(length=150), nullable=True),
    sa.Column('status', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('tags',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('tags_name', sa.String(length=30), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_table('tags')
    op.drop_table('roles')
    op.drop_table('pynews')
    op.drop_table('article')
    op.drop_table('access_log')
    # ### end Alembic commands ###
