from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField
from wtforms.validators import Length, Email, EqualTo

class SignupForm(FlaskForm):
    """validates the signup forms"""
    name = StringField(label="User Name: ", validators=Length(min=2, max=60))
    email = StringField(label="Email Address: ", validators=Length(max=100))
    number = IntegerField(label="Phone Number: ")
    password1 = PasswordField(label="Password: ", validators=Length(max=60))
    password2 = PasswordField(label="Confirm Password: ", validators=EqualTo("password1"))
    submit = SubmitField(label="Create Account")