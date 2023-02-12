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
    RECAPTCHA_PRIVATE_KEY = '6LfDe1gkAAAAAMlKVfQT1qcVJRhZLdlekY0CTCW2'
    RECAPTCHA_OPTIONS = {'theme': 'black'}

    # Mail
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587  # or 465 - for SSL or 25
    MAIL_USE_TLS = True
    MAIL_USERNAME = environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = environ.get('MAIL_PASSWORD')


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    DEBUG = True
    # For UNIT tests
    # TESTING = True
