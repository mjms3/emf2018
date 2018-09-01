"""Basic results structure

Revision ID: a3f24e3fc622
Revises: b429dd922bae
Create Date: 2018-08-26 14:27:57.729867

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
from textwrap import dedent

revision = 'a3f24e3fc622'
down_revision = 'b429dd922bae'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('login_user',
    sa.Column('login_user_id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('login_user_id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('request_token',
    sa.Column('request_token_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('request_token', sa.String(), nullable=False),
    sa.Column('requested_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['login_user.login_user_id'], ),
    sa.PrimaryKeyConstraint('request_token_id'),
    sa.UniqueConstraint('request_token')
    )
    op.create_table('submitted_result',
    sa.Column('submitted_result_id', sa.Integer(), nullable=False),
    sa.Column('request_token_id', sa.Integer(), nullable=False),
    sa.Column('result_value', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['request_token_id'], ['request_token.request_token_id'], ),
    sa.PrimaryKeyConstraint('submitted_result_id')
    )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('submitted_result')
    op.drop_table('request_token')
    op.drop_table('login_user')
    # ### end Alembic commands ###