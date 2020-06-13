import csv
import os
from passlib.hash import sha256_crypt
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv('DATABASE_URL'))
db = scoped_session(sessionmaker(bind=engine))


def check(name, password):
    y = db.execute("select * from users where name=:name",
                   {"name": name}).fetchone()
    p = password
    if y == None:
        return "Username doesn't exist try again"
    else:
        if y.password==p:
            return "sucess"
        else:
            return "Username and password do not match"
