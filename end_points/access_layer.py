from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def _get_session():
    engine = create_engine('postgresql://wwwuser:wwwuser@localhost/emf2018_db', echo=False)
    Session = sessionmaker(bind=engine)
    return Session()