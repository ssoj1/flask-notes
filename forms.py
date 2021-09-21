"""Forms for List app."""

from wtforms.fields.simple import PasswordField
from wtforms.validators import InputRequired, Optional, Email, Length, DataRequired
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, BooleanField

class RegisterForm(FlaskForm):
    """Register a new user"""

    username = StringField("Username", 
                            validators=[InputRequired(), 
                            Length(max=20)
                            ])
    password = PasswordField("Password", 
                            validators=[DataRequired(), 
                            Length(max=100)
                            ])
    email = StringField("Email Address", 
                            validators=[InputRequired(), 
                            Email(), 
                            Length(max=50)
                            ])
    first_name = StringField("First Name", 
                            validators=[InputRequired(), 
                            Length(max=30)
                            ])
    last_name = StringField("Last Name", 
                            validators=[InputRequired(), 
                            Length(max=30)
                            ])

class LogInForm(FlaskForm):
    """ Logs in an existing user """

    username = StringField("Username", 
                            validators=[InputRequired(), 
                            Length(max=20)
                            ])
    password = PasswordField("Password", 
                            validators=[DataRequired(), 
                            Length(max=100)
                            ])
