from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from flaskblog.models import AppUser


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=20)]
    )
    email = StringField(label="Email", validators=[DataRequired(), Email()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        label="Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField(label="Sign Up!")

    def validate_username(self, username):
        user = AppUser.query.filter_by(username=username.data).first()
        # IF user is not None...
        if user:
            raise ValidationError("That username is taken! Please use a different one.")

    def validate_email(self, email):
        user = AppUser.query.filter_by(email=email.data).first()
        # If user is not None... (the user already exists)
        if user:
            raise ValidationError("That email is taken! Please use a different one.")


class LoginForm(FlaskForm):
    email = StringField(label="Email", validators=[DataRequired(), Email()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    remember = BooleanField(label="Remember Me")
    submit = SubmitField(label="Login")


class UpdateAccountForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=20)]
    )
    email = StringField(label="Email", validators=[DataRequired(), Email()])
    picture = FileField(
        label="Update Profile Picture", validators=[FileAllowed(["jpg", "png"])]
    )
    submit = SubmitField(label="Update")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = AppUser.query.filter_by(username=username.data).first()
            # IF user is not None...
            if user:
                raise ValidationError(
                    "That username is taken! Please use a different one."
                )

    def validate_email(self, email):
        if email.data != current_user.email:
            email = AppUser.query.filter_by(email=email.data).first()
            # IF email is not None... (the email already exists)
            if email:
                raise ValidationError(
                    "That email is taken! Please use a different one."
                )


class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = TextAreaField(label="Content", validators=[DataRequired()])
    submit = SubmitField(label="Create Post")


class RequestResetForm(FlaskForm):
    email = StringField(label="Email", validators=[DataRequired(), Email()])
    submit = SubmitField(label="Request Password Reset")

    def validate_email(self, email):
        user = AppUser.query.filter_by(email=email.data).first()
        # If user is None... (the user does not exist)
        if user is None:
            raise ValidationError(
                "There is no registered account attached to this email."
            )


class ResetPasswordForm(FlaskForm):
    password = PasswordField(label="Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        label="Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField(label="Reset Password")
