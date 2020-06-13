import csv
import os
from passlib.hash import sha256_crypt
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv('DATABASE_URL'))
db = scoped_session(sessionmaker(bind=engine))  



def signup(name,password):
    y=db.execute("select * from users where name=:name",{"name":name}).fetchone()
    if y!=None:
        return "Username already taken, try other username"
    else:
        #password = sha256_crypt.encrypt(password)
        db.execute("insert into users(name,password) values (:name,:password)",{"name":name,"password":password})
        db.commit()
        return "Account Created proceed to login"
