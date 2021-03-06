"""empty message

Revision ID: 993b2e5bcc11
Revises: 
Create Date: 2017-12-10 15:07:52.729671

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '993b2e5bcc11'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('reciever',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('email_id', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('results_2',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('url', sa.String(), nullable=True),
    sa.Column('result_all', postgresql.JSON(astext_type=sa.Text()), nullable=True),
    sa.Column('result_no_stop_words', postgresql.JSON(astext_type=sa.Text()), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('user_name', sa.String(length=200), nullable=False),
    sa.Column('email_id', sa.String(length=100), nullable=False),
    sa.Column('tokens', sa.Text(), nullable=True),
    sa.Column('credentials', postgresql.JSON(astext_type=sa.Text()), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('campaigns',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('campaign_name', sa.String(length=100), nullable=False),
    sa.Column('day_flow', postgresql.JSON(astext_type=sa.Text()), nullable=True),
    sa.Column('mail_info', postgresql.JSON(astext_type=sa.Text()), nullable=True),
    sa.Column('user', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['user'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('campaign_name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('campaigns')
    op.drop_table('user')
    op.drop_table('results_2')
    op.drop_table('reciever')
    # ### end Alembic commands ###
