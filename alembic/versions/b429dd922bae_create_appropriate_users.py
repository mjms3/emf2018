"""Create appropriate users

Revision ID: b429dd922bae
Revises: 
Create Date: 2018-08-26 13:20:19.497048

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b429dd922bae'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""\
    REVOKE ALL PRIVILEGES ON DATABASE emf2018_db FROM public;
    CREATE ROLE wwwuser NOSUPERUSER NOCREATEDB NOCREATEROLE INHERIT LOGIN;
    """)


def downgrade():
    op.execute("""\
    DROP ROLE IF EXISTS wwwuser;
    GRANT ALL PRIVILEGES ON DATABASE emf2018_db TO public;
    """)
