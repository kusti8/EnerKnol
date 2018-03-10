from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

eng = create_engine('sqlite:///users.db')

Base = declarative_base()


class User(Base):
    __tablename__ = 'Users'

    Id = Column(Integer, primary_key=True)
    Username = Column(String)
    Password = Column(String)
    FirstName = Column(String)
    LastName = Column(String)
    Email = Column(String)

Base.metadata.bind = eng
Base.metadata.create_all()