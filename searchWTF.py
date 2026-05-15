from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, RadioField, SelectField
from wtforms.validators import DataRequired, Email, Length, NumberRange, Regexp, URL, InputRequired
from models.getauthors import getauthors

class AskForTitle(FlaskForm):
    book_title = StringField('Enter Book Title to Search for: ', validators=[DataRequired()])

class AskForAuthor(FlaskForm):
    book_author = StringField('Enter Author Name to Search for: ', validators=[DataRequired()])
    
class AskForYear(FlaskForm):
    book_year = StringField('Enter Year to Search for: ', validators=[DataRequired()])

class GetAuthors(FlaskForm):
    with open("stuff.inc") as pwfile:
        mydata = pwfile.readline()
        mydata = mydata.rstrip('\n')
        dblist = mydata.split(" ")
        dbtuple = tuple(dblist)
        dbpasswd, dbuser, dbname = dbtuple
    author_list = getauthors('',dbuser, dbpasswd, dbname)
    author_list.insert(0,(None, "Choose an Author!"))
    choose_author = SelectField("Choose your Author", choices=author_list, validators=[DataRequired()])
    submit = SelectField("Search by Author")
        
class NewUsers (FlaskForm):
    first_name = StringField('First Name:', validators=[DataRequired()])
    
    
class LoginUsers(FlaskForm):
    pass
    
