import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv('DATABASE_URL'))
db = scoped_session(sessionmaker(bind=engine))  


def main():
    db.execute("create table books (id serial primary key, isbn varchar not null,title varchar not null,author varchar not null,year varchar not null)")
    with open('books.csv','r') as book:
        f= csv.reader(book)
        next(f)
        i=0
        for isbn,title,author,year in f:
            db.execute("insert into books(isbn,title,author,year) values(:isbn,:title,:author,:year)",{"isbn":isbn,"title":title,"author":author,"year":year})
            print(i)
            i+=1
    db.commit()
if __name__=='__main__':
    main()