from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, RadioField, SelectField
from wtforms.validators import DataRequired, Email, Length, NumberRange, Regexp, URL, InputRequired

class AskForTitle(FlaskForm):
    book_title = StringField('Enter Book Title to Search for: ', validators=[DataRequired()])
