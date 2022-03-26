from email import message
from sqlalchemy import Column, String, Integer, Enum
from sqlalchemy.ext.declarative import declarative_base

base = declarative_base()


class Message(base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    message = Column(String)
