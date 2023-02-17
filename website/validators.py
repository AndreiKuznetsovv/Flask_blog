from wtforms.validators import (
    ValidationError,
)

from .models import User


# custom validator for check whether user and email exists or not
def FieldAlreadyExist(form, field):
    if field.name == 'username':
        field_exists = User.query.filter_by(username=field.data).first()
    else:
        field_exists = User.query.filter_by(email=field.data).first()

    if field_exists:
        raise ValidationError(f'That {field.name.capitalize()} is taken. Please choose a different one.')


def EmailNotExist(form, email):
    email_exists = User.query.filter_by(email=email.data).first()

    if not email_exists:
        raise ValidationError('This email does\'t exist')
