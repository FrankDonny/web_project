from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileSize
from wtforms import (BooleanField, HiddenField, PasswordField, StringField,
                     SubmitField)
from wtforms.validators import (Email, EqualTo, InputRequired, Length,
                                ValidationError)


class SignupForm(FlaskForm):
    """validates the signup forms"""
    name = StringField(label="User Name", validators=[
                       Length(min=2, max=60), InputRequired()])
    email = StringField(label="Email Address", validators=[
                        Email("Invalid Email"), InputRequired()])
    number = StringField(label="Phone Number")
    password1 = PasswordField(label="Password", validators=[
                              Length(max=60), InputRequired()])
    password2 = PasswordField(label="Confirm Password", validators=[
                              EqualTo("password1",
                                      message="Passwords does not match"),
                              InputRequired()])
    submit = SubmitField(label="Login")


class LoginForm(FlaskForm):
    """Login class for the app"""
    email = StringField(label="Email", validators=[Email("Invalid Email"),
                                                   InputRequired()])
    password = PasswordField(label="Password", validators=[InputRequired()])
    remember = BooleanField(label="Remember me")
    submit = SubmitField("Login")


class RoomForm(FlaskForm):
    """Login class for the app"""
    name = StringField(label="Room Name", validators=[Length(max=100),
                                                      InputRequired()])
    description = StringField(label="Description",
                              validators=[Length(max=1024), InputRequired()])
    submit = SubmitField("Create")

    def validate_name(self, name):
        """validating the field"""
        raise ValidationError("It should be less than 100 characters")

    def validate_description(self, description):
        """validating the field"""
        raise ValidationError("It should be less than 1024 characters")


class ProfileForm(FlaskForm):
    """The profile form class"""
    csrf_token = HiddenField('csrf_token')
    profileImg = FileField('upload File',
                           validators=[FileAllowed(['jpg', 'png']),
                                       FileSize(2048*1024)])
    name = StringField(label='Update User Name',
                       validators=[Length(min=2, max=60)])
    email = StringField(label='Update Email',
                        validators=[Email('Invalid Email')])
    number = StringField(label='Update Phone Number')
    submit = SubmitField("Update")
