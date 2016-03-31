from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, PasswordField, TextField
from wtforms.validators import Required
from wtforms import validators, ValidationError
from wtforms.validators import DataRequired


class LoginForm(Form):
    
    email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)
