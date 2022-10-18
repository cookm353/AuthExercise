from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.widgets import PasswordInput
from wtforms.validators import InputRequired, Email, Length

class RegistrationForm(FlaskForm):
    """Form for registering"""
    username = StringField('Username', 
                           validators=[InputRequired(message='Please enter a username'), Length(max=20)])
    password = StringField('Password',
                           widget=PasswordInput(), validators=[InputRequired(message='Please enter a password')])
    email = StringField('Email', validators=[InputRequired(message='Please enter a valid email address'), 
                                             Email(message='Please enter a valid email address'),
                                             Length(max=50)])
    first_name = StringField('First name', validators=[InputRequired(message='Please enter your first name'),
                                                       Length(max=30)])
    last_name = StringField('Last name', validators=[InputRequired(message='Please enter your last name'),
                                                     Length(max=30)])
    
class LoginForm(FlaskForm):
    """Form for logging in"""
    username = StringField('Username', validators=[InputRequired('Please enter a username')])
    password = StringField('Password', widget=PasswordInput(), validators=[InputRequired('Please enter a password')])
    
class FeedbackForm(FlaskForm):
    """Form for leaving feedback"""
    ...