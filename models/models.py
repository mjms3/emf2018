from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, Numeric
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class LoginUser(Base):
    __tablename__ = 'login_user'

    login_user_id = Column(Integer,primary_key=True)
    username = Column(String,unique=True, nullable=False)
    age = Column(Integer, nullable=False)
    tag_line = Column(String, nullable=False)
    temperature = Column(Numeric, nullable=False)
    humidity = Column(Numeric, nullable=False)
    magnetic_flux = Column(Numeric, nullable =False)
