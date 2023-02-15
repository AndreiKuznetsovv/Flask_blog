from os import path, environ

from dotenv import load_dotenv

"""Flask configuration."""

basedir = path.abspath(path.dirname(__file__))
# load dotenv from '/home/dron/PycharmProjects/flaskProjects/flask_blog/.env'
load_dotenv(path.join(basedir, '../.env'))


class Config(object):
    """Set Flask config variables."""
    SECRET_KEY = environ.get('SECRET_KEY')

    # Database
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')

    # Recaptcha
    RECAPTCHA_PUBLIC_KEY = '6LfDe1gkAAAAAJ1VpcKubUCtmHz2rMMYFO5i51Ng'
    RECAPTCHA_PRIVATE_KEY = environ.get('RECAPTCHA_PRIVATE_KEY')
    RECAPTCHA_OPTIONS = {'theme': 'black'}

    # Mail
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587  # or 465 - for SSL or 25
    MAIL_USE_TLS = True
    MAIL_USERNAME = environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = environ.get('MAIL_PASSWORD')

    # OAuth (NOT IMPLEMENTED RIGHT NOW)
    GOOGLE_CLIENT_ID = environ.get('CLIENT_ID')
    GOOGLE_CLIENT_SECRET = environ.get('CLIENT_SECRET')
    OAUTHLIB_INSECURE_TRANSPORT = "1"


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    DEBUG = True
    # For UNIT tests
    # TESTING = True
