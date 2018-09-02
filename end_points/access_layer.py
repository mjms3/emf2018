import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool


def _get_session():
    connection_string = 'postgresql://wwwuser:wwwuser@{}/emf2018_db'
    db = os.environ.get('DB_NAME', 'localhost')
    engine = create_engine(connection_string.format(db), echo=False, poolclass=NullPool)
    Session = sessionmaker(bind=engine)
    return Session()