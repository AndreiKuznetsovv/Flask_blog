import os
import secrets

from PIL import Image
from flask import url_for, current_app
from flask_mail import Message

from website.models import UserInfo, mail


def save_image(form_image):
    # creating a random hex value for image name
    random_hex = secrets.token_hex(8)
    # get the filename and the extension of the user image
    _, f_ext = os.path.splitext(form_image.filename)
    image_filename = random_hex + f_ext
    image_path = os.path.join(current_app.root_path, 'static/profile_pics', image_filename)
    # resize image
    output_size = (125, 125)
    resize_image = Image.open(form_image)
    resize_image.thumbnail(output_size)
    # save our image
    resize_image.save(image_path)
    return image_filename


def send_reset_email(user: UserInfo):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com', recipients=[user.email])
    msg.body = f'''
    To reset your password, visit the following link:
    {url_for('.reset_token', token=token, _external=True)}

    If you did not make this request then simply ignore this message and no changes will be made.
    '''
    mail.send(msg)
