from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
import os

eng = create_engine(os.environ['MYSQL_URL'])

Base = declarative_base()


class User(Base):
    __tablename__ = 'Users'

    Id = Column(Integer, primary_key=True)
    Username = Column(String(200))
    Password = Column(String(200))
    FirstName = Column(String(200))
    LastName = Column(String(200))
    Email = Column(String(200))
    Favorites = Column(String(1000))

Base.metadata.bind = eng
Base.metadata.create_all()