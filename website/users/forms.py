from flask_login import current_user
from flask_wtf import (
    FlaskForm, RecaptchaField,
    Recaptcha,
)
from flask_wtf.file import (
    FileField, FileAllowed,
)
from wtforms import (
    StringField, PasswordField,
    SubmitField, BooleanField,
)
from wtforms.validators import (
    DataRequired, Length,
    Email, EqualTo, ValidationError,
)

from website.models import User
from website.validators import (
    FieldAlreadyExist,
    EmailNotExist,
)


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=3, max=20), FieldAlreadyExist])
    email = StringField('Email',
                        validators=[DataRequired(), Email(), FieldAlreadyExist])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    recaptcha = RecaptchaField(validators=[Recaptcha(message='You\'re not a robot... are you?')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email(), EmailNotExist])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    remember = BooleanField('Remember me')
    recaptcha = RecaptchaField(validators=[Recaptcha(message='You\'re not a robot... are you?')])
    submit = SubmitField('Login')

    def validate_recaptha(self, recaptcha):
        if not recaptcha.data:
            raise ValidationError('Recaptcha is required')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    image = FileField('Update Profile Picture',
                      validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def update_account_email(self, email):
        if current_user.email != email.data:
            email_exists = User.query.filter_by(email=email.data).first()
            if email_exists:
                raise ValidationError(f'That email is taken. Please choose a different one.')

    def update_account_username(self, username):
        if current_user.username != username.data:
            username_exists = User.query.filter_by(username=username.data).first()
            if username_exists:
                raise ValidationError((f'That username is taken. Please choose a different one.'))


class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email(), EmailNotExist])
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
