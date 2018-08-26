"""Create appropriate users

Revision ID: b429dd922bae
Revises: 
Create Date: 2018-08-26 13:20:19.497048

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
from textwrap import dedent

revision = 'b429dd922bae'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute(dedent("""\
    REVOKE ALL PRIVILEGES ON DATABASE emf2018_db FROM public;
    DROP ROLE IF EXISTS wwwuser;
    CREATE ROLE wwwuser NOSUPERUSER NOCREATEDB NOCREATEROLE INHERIT LOGIN PASSWORD 'wwwuser';
    GRANT CONNECT ON DATABASE emf2018_db TO wwwuser;
    alter default privileges in schema public grant select, insert, update, delete on tables to wwwuser;
    alter default privileges in schema public grant usage on sequences to wwwuser;
    """))


def downgrade():
    op.execute(dedent("""\
    DROP ROLE IF EXISTS wwwuser;
    GRANT ALL PRIVILEGES ON DATABASE emf2018_db TO public;
    """))
