from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class LoginUser(Base):
    __tablename__ = 'login_user'

    login_user_id = Column(Integer,primary_key=True)
    username = Column(String,unique=True, nullable=False)

class RequestToken(Base):
    __tablename__ = 'request_token'

    request_token_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('login_user.user_id'), nullable=False)
    request_token = Column(String, unique=True, nullable=False)
    requested_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

class SubmittedResult(Base):
    __tablename__ = 'submitted_result'

    submitted_result_id = Column(Integer, primary_key=True)
    request_token_id = Column(Integer, ForeignKey('request_token.request_token_id'), nullable=False)
    result_value = Column(Integer, nullable=False)
