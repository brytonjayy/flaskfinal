from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, RadioField, SelectField
from wtforms.validators import DataRequired, Email, Length, NumberRange, Regexp, URL, InputRequired

class AskForTitle(FlaskForm):
    book_title = StringField('Enter Book Title to Search for: ', validators=[DataRequired()])

class AskForAuthor(FlaskForm):
    book_author = StringField('Enter Author Name to Search for: ', validators=[DataRequired()])
    
class AskForYear(FlaskForm):
    book_year = StringField('Enter Year to Search for: ', validators=[DataRequired()])