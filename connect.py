from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


class Base(DeclarativeBase):
    pass


DB_URL = "postgresql://postgres:university@localhost/postgres"

engine = create_engine(DB_URL)

DBSession = sessionmaker(bind=engine)
session = DBSession()