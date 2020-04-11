from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo
def validate_portnumber(form, field):
    if 0 > field.data > 65535:
        raise ValueError("Invalid port number.")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(message="Username can not be empty"),
                                                   Length(min=2, message="Username must at least be 2 characters long")])
    password = PasswordField("Password", validators=[InputRequired(message="Password can not be empty"),
                                                     Length(min=5, message="Password must at least be 5 characters long")])
    remember = BooleanField("Keep logged in")
    submit = SubmitField("Login")


class ChangePasswordForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=1, max=20)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=5, max=20)])
    confirm_password = PasswordField("Confirm Password", validators=[InputRequired(), EqualTo("password")])
    submit = SubmitField("Change Login Data")