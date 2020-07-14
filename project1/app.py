from flask import Flask, render_template, jsonify, request , redirect ,url_for, session
import os
from flask_api import status
app = Flask(__name__)
from flask_session import Session
from helper_reg import signup
from helper_login import check
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from helper_api import ratings
engine = create_engine(os.getenv('DATABASE_URL'))
db = scoped_session(sessionmaker(bind=engine))
app.secret_key = os.urandom(24)
#login route
@app.route("/",methods=["GET","POST"])
def login():
    if request.method == 'GET':
        message=None
        return render_template('index.html',message=message)
    else:
        name=request.form.get('uname')
        password=request.form.get('password')
        x=check(name,password)
        if x=="sucess":
            session['loggedin']= True
            session['username']=name
            return redirect(url_for('books')) #(IMP) CANNOT REDIRECT DIRECTLY TO DASHBOARD AND THEN GET VALUES OF SEARCH BAR BY DEFNINING GET METHOD IN BOOK AS
            #WHEN IT WILL LOAD DASHBOARD FOR FIRST TIME THAT WILL BE GET REQUEST AND SEARCH BAR WILL RETURN NONE. WE SEARCH AFTER THAT .  
        else:
            return render_template("index.html",message=x)
@app.route("/register",methods=["GET","POST"])#keep get an post capital
def register():
    if request.method == 'POST':
        name=request.form.get('uname')
        password=request.form.get('password')
        x=signup(name,password)#made a helper file and imported function
        return render_template('signup.html',message=x)
    else:
        message=None
        return render_template('signup.html',message=message)

@app.route("/books",methods=["GET","POST"])
def books():
    if request.method=='POST':#REFER LOGIN TO SEE WHY THIS ISN'T PUT IN GET
        query=request.form.get('sir')
        query="%"+query.lower()+"%" #made the search lowercase and likewise changed sql query to get optimal matching. because Dark and dark would not match even in like it would search for "%dark%" and db has "%Dark%" therefore converted both to lower. 
        #note both could have been converted to upper as well
        li=db.execute("select * from books where lower(isbn) like :query or lower(title) like :query or lower(author) like :query",{"query":query}).fetchall()
        ret=[]
        for i in li:# as fetchall returns 2-d list so can be accessed as l[0].name but if fetchone is used can either use l[0] or l.name as only one row is there 
            ret.append(i.title)
        return render_template("dashboard.html",ret=ret)
    else:
        return render_template("dashboard.html")
    
@app.route("/books/<bname>",methods=["GET","POST"])
def details(bname):
    if request.method=='GET':
        x=db.execute("select * from rating where bid=:bname",{"bname":bname}).fetchall()
        lis=[]
        if x!=None:
            for i in x:
                li=[]
                li.append(i.uid)
                li.append(i.detail)
                lis.append(li)
        l=db.execute("select * from books where title=:bname",{"bname":bname}).fetchone()#for getting isbn which will be used to get data from goodreads
        ret=ratings(l.isbn)# function called from helper_api
        message=None
        return render_template("review.html",bname=bname,l=l,ret=ret,lis=lis,message=message)
    else:
        uid=session['username']
        bid=bname
        res=db.execute("select * from rating where uid=:uid and bid=:bid",{"uid":uid,"bid":bid}).fetchone()
        if res != None:
            message= "Already Submitted review for this book"
            return render_template('review.html',message=message)
        else:
            rating=request.form.get('rating')
            detail=request.form.get('review')
            db.execute("insert into rating(rating,detail,uid,bid) values(:rating,:detail,:uid,:bid)",{'rating':rating,"detail":detail,"uid":uid,"bid":bid})
            db.commit()
            message="Thanks for review your data has been submitted "
            return render_template('review.html',message=message)
@app.route('/logout',methods=['GET'])
def logout():
    session.pop('username',None)
    session.pop('loggedin',None)
    message="Logged out, Log in again."
    return render_template('index.html',message=message) # already for incorrect login same variable with different message is passed in login route('/') thus no change was required in index.html.
        
@app.route('/api/<isbn>',methods=['GET']) #add a not 404 resource not fouund message
def api(isbn):
    result=db.execute("select * from books where isbn=:isbn",{"isbn":isbn}).fetchone()
    dicto={}
    dicto['title']=result.title
    dicto['isbn']=result.isbn
    dicto['author']=result.author
    dicto['year']=result.year
    reto=ratings(isbn)
    dicto['review_count']=reto['number_ratings']
    dicto['average_score']=reto['average_rating']
    return jsonify(dicto)

if __name__=='__main__':
    app.run(debug=True)
    
