import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv('DATABASE_URL'))
db = scoped_session(sessionmaker(bind=engine))  


def signup(name,password):
    db.execute("insert into users(name,password) values (:name,:password)",{"name":name,"password":password})
    db.commit()
    return "success"
