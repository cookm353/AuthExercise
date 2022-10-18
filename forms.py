from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.widgets import PasswordInput
from wtforms.validators import InputRequired, Email

class RegistrationForm(FlaskForm):
    """Form for registering"""
    username = StringField('Username', validators=[InputRequired('Please enter a username')])
    password = StringField('Password', widget=PasswordInput(), validators=[InputRequired('Please enter a password')])
    email = StringField('Email', validators=[InputRequired('Please enter a valid email address'), 
                                             Email('Please enter a valid email address')])
    first_name = StringField('First name', validators=[InputRequired('Please enter your first name')])
    last_name = StringField('Last name', validators=[InputRequired('Please enter your last name')])
    
class LoginForm(FlaskForm):
    """Form for logging in"""
    username = StringField('Username', validators=[InputRequired('Please enter a username')])
    password = StringField('Password', widget=PasswordInput(), validators=[InputRequired('Please enter a password')])
    
class FeedbackForm(FlaskForm):
    """Form for leaving feedback"""
    ...