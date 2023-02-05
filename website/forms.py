from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    StringField, PasswordField,
    SubmitField, BooleanField,
    TextAreaField,
)
from wtforms.validators import (
    DataRequired, Length,
    Email, EqualTo, ValidationError,
)
from flask_login import current_user
from .models import UserInfo


# custom validations for check whether user and email exists or not
def FieldAlreadyExist(form, field):
    if field.name == 'username':
        field_exists = UserInfo.query.filter_by(username=field.data).first()
    else:
        field_exists = UserInfo.query.filter_by(email=field.data).first()

    if field_exists:
        raise ValidationError(f'That {field.name.capitalize()} is taken. Please choose a different one.')


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=3, max=20), FieldAlreadyExist])
    email = StringField('Email',
                        validators=[DataRequired(), Email(), FieldAlreadyExist])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')

    def validate_email(self, email):
        email_exists = UserInfo.query.filter_by(email=email.data).first()

        if not email_exists:
            raise ValidationError('This email does\'t exist')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Text', validators=[DataRequired()])
    submit = SubmitField('Post')


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
            email_exists = UserInfo.query.filter_by(email=email.data).first()
            if email_exists:
                raise ValidationError(f'That email is taken. Please choose a different one.')

    def update_account_username(self, username):
        if current_user.username != username.data:
            username_exists = UserInfo.query.filter_by(username=username.data).first()
            if username_exists:
                raise ValidationError((f'That username is taken. Please choose a different one.'))


class CommentForm(FlaskForm):
    content = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Submit')
