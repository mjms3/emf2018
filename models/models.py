from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, Numeric, CheckConstraint, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class LoginUser(Base):
    __tablename__ = 'login_user'

    login_user_id = Column(Integer,primary_key=True)
    username = Column(String, nullable=False)
    unique_identifier = Column(String, nullable=False, unique=True)
    age = Column(Integer, nullable=False)
    tag_line = Column(String, nullable=False)
    temperature = Column(Numeric, nullable=True)
    humidity = Column(Numeric, nullable=True)
    magnetic_flux = Column(Numeric, nullable =True)
    looking_for = Column(String, nullable=False)
    contact = Column(String, nullable=False)


class Match(Base):
    __tablename__ = 'match'

    match_id = Column(Integer, primary_key=True)
    user_1 = Column(Integer, ForeignKey('login_user.login_user_id'), nullable=False)
    user_2 = Column(Integer, ForeignKey('login_user.login_user_id'), nullable=False)
    status = Column(String, nullable=False)

    __table_args__ = (UniqueConstraint('user_1', 'user_2', name='matches_unique_constraint'),
                      CheckConstraint("status in ('matched', 'not_matched')", name='check_match_status'),
                      )