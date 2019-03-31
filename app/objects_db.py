import sqlalchemy
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base

from config_db import config

base = declarative_base()

# "storage location" environment variables
uri = "sqlite:///" + config['STORAGE_LOCATION'] + "user.db"
engine = sqlalchemy.create_engine(uri)
base.metadata.bind = engine
Session = orm.sessionmaker(bind=engine)
session: orm.session.Session = Session()
