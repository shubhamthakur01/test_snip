import os
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from wtforms.fields import EmailField, SelectField


basedir = os.path.abspath(os.path.dirname(__file__))
# SQL connection string
sql_connection_string = os.environ['SQL_STRING']

class Config(object):
    SECRET_KEY=os.urandom(24)
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'week5.db')
    SQLALCHEMY_DATABASE_URI = sql_connection_string
    SQLALCHEMY_TRACK_MODIFICATIONS = True # flask-login uses sessions which require a secret Key


class RegistrationForm(FlaskForm):
    email_err = "Invalid email format, Valid format: xxxx@xxxx.xxx"
    firstname = StringField('First Name ', validators=[DataRequired()])
    lastname = StringField('Last Name ', validators=[DataRequired()])
    email = EmailField('Email Id ', validators=[DataRequired(),
                                                Email(message=email_err)])
    password = PasswordField('Enter Password',
                             validators=[DataRequired(),
                                         Length(min=6, max=40)])
    confirm = PasswordField('Confirm Password ',
                            validators=[DataRequired(), EqualTo('password')])
    gender = SelectField('Gender ', choices=['Male', 'Female', 'Others'])
    location = SelectField('Location ', choices=['USA', 'India', 'Others'])
    submit = SubmitField('Sign Up ')


class LogInForm(FlaskForm):
    email_err = "Invalid email format, Valid format: xxxx@xxxx.xxx"
    email = EmailField('Email Id ', validators=[DataRequired(),
                                                Email(message=email_err)])
    password = PasswordField('Password ', validators=[DataRequired(),
                                                      Length(min=6, max=40)])
    submit = SubmitField('Login')
