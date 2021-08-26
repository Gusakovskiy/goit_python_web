from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
_CONNECTION = 'postgresql://postgres:qwe123@localhost/personal_assistant'

engine = create_engine(_CONNECTION, echo=True)
metadata = Base.metadata
DBSession = sessionmaker(bind=engine)
session = DBSession()
