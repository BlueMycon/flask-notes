from wtforms import StringField, PasswordField
from flask_wtf import FlaskForm

from wtforms.validators import InputRequired, Length, Email

class RegistrationForm(FlaskForm):
    """Registration form."""
    username = StringField(
        "Username",
        validators=[InputRequired(),Length(max=20)])

    password = PasswordField(
        "Password",
        validators=[InputRequired(),Length(max=100)])

    email = StringField(
        "Email",
        validators=[InputRequired(),Length(max=50), Email(message="Please enter a valid email.")])

    first_name = StringField(
        "First Name",
        validators=[InputRequired(),Length(max=30)])

    last_name = StringField(
        "Last Name",
        validators=[InputRequired(),Length(max=30)])


class LoginForm(FlaskForm):
    """Login form."""
    username = StringField(
        "Username",
        validators=[InputRequired(),Length(max=20)])

    password = PasswordField(
        "Password",
        validators=[InputRequired(),Length(max=100)])

class CSRFProtectForm(FlaskForm):
    """Form just for CSRF Protection"""
