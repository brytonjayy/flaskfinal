from flask import Flask, render_template, url_for, request
from searchWTF import AskForTitle
from models.bytitlesearch import getbooks

app = Flask(__name__)
app.secret_key = b'(YPT#{@#YAS^RPPF#TA#DGA#adsg' # This should be protected ie don't record it on zoom ;)
app.config.from_object(__name__)

@app.route('/')
def index():
    return render_template ('index.html')

@app.route("/bytitle")
def bytitle():
    title_form = AskForTitle()
    return render_template ('bytitle.html', form=title_form)

@app.route('/titles', methods=['POST'])
def list_of_titles():
    with open("stuff.inc") as pwfile:
        mydata = pwfile.readline()
        mydata = mydata.rstrip('\n')
        dblist = mydata.split(" ")
        dbtuple = tuple(dblist)
        dbpasswd, dbuser, dbname = dbtuple

    searchby = request.form['book_title']
    # searchby = request.args['book_title']
    books = getbooks(searchby,dbuser,dbpasswd,dbname)

    return books

# @app.route('/login', methods=['GET','POST'])
# def logthemin():
#     form = LoginUsers()
    

if __name__ == '__main__':
    app.run(debug=True)
    
