import mysql.connector.errors
from flask import Flask, render_template, url_for, request, redirect
# from searchWTF import AskForTitle, AskForYear, GetAuthors, NewUsers, LoginUsers
from searchWTF import AskForTitle, AskForYear, GetAuthors
from models.bytitlesearch import getbooks
from models.byyearsearch import getbooksbyyear
from models.bookinfo import getbookinfo
from models.byauthorid import getbooksbyauthid
# from models.createuser import newuser
# from models.getuser import retrieveuser
from flask_session import Session
from flask import session
from flask_argon2 import Argon2
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = b'(YPT#{@#YAS^fkfieonerngps'
SESSION_TYPE='filesystem'
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True
app.config.from_object(__name__)
Session(app)
argon2 = Argon2(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template ('index.html')

@app.route("/bytitle", methods=['GET', 'POST'])
def bytitle():
    title_form = AskForTitle()

    return render_template ('bytitle.html', form=title_form)

@app.route('/titles', methods=['GET', 'POST'])
def list_of_titles():
    with open("stuff.inc") as pwfile:
        mydata = pwfile.readline()
        mydata = mydata.rstrip('\n')
        dblist = mydata.split(" ")
        dbtuple = tuple(dblist)
        dbpasswd, dbuser, dbname = dbtuple

    searchby = request.form['book_title']

    books = getbooks(searchby,dbuser,dbpasswd,dbname)
    title = "Books By Title"
    return render_template('books.html', title=title, data=books)

@app.route('/byyear',methods=['GET', 'POST'])
def byyearsearch(year=None):
    if request.method == 'POST':
        byear = request.form['book_year']
        byear = '/year/' + byear
        return redirect(byear)
    else:
        year_form = AskForYear()
        return render_template('byyear.html', form=year_form)

@app.route('/year/<byyear>', methods=['GET', 'POST'])
def booksbyyear(byyear=None):
    with open("stuff.inc") as pwfile:
        mydata = pwfile.readline()
        mydata = mydata.rstrip('\n')
        dblist = mydata.split(" ")
        dbtuple = tuple(dblist)
        dbpasswd, dbuser, dbname = dbtuple
    books = getbooksbyyear(byyear, dbuser, dbpasswd, dbname)
    title= f"Books By from the year {byyear}"
    return render_template('books.html', title=title, data=books)

@app.route('/bookinfo/<bookid>', methods=['GET', 'POST'])
def bookinfo(bookid=None):
        with open("stuff.inc") as pwfile:
            mydata = pwfile.readline()
            mydata = mydata.rstrip('\n')
            dblist = mydata.split(" ")
            dbtuple = tuple(dblist)
            dbpasswd, dbuser, dbname = dbtuple
        bookstuff = getbookinfo(bookid,dbuser,dbpasswd,dbname)
        return render_template('bookinfo.html', title="Book Information", data=bookstuff)

@app.route('/byauthor', methods=['GET','POST'])
def showauthors():
    form = GetAuthors()
    if request.method == 'POST':
        if request.form['choose_author'] == None:
            return "Failed to choose an author"
        
        authorid = request.form['choose_author']
        with open("stuff.inc") as pwfile:
            mydata = pwfile.readline()
            mydata = mydata.rstrip('\n')
            dblist = mydata.split(" ")
            dbtuple = tuple(dblist)
            dbpasswd, dbuser, dbname = dbtuple
        books = getbooksbyauthid(authorid, dbuser, dbpasswd, dbname)
        return render_template ('books.html', data= books)
    else:
        return render_template('byauthors.html', form= form)

@app.route('/newuser',methods=['GET','POST'])
def create_user():
    if request.method == 'POST':
        return "Process form"
    else:
        return "Show form"


if __name__ == '__main__':
    app.run()
    
    




    
