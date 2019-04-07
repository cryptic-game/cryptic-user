import os

from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative.api import DeclarativeMeta
from sqlalchemy.orm import sessionmaker

from config import config

directory: str = config["STORAGE_LOCATION"]

if not os.path.exists(directory):
    os.makedirs(directory)

engine: Engine = create_engine('sqlite:///' + directory + 'user.db')
Session: sessionmaker = sessionmaker(bind=engine)
Base: DeclarativeMeta = declarative_base()
session: Session = Session()
