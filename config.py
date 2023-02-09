from os import path, environ
from dotenv import load_dotenv

"""Flask configuration."""

basedir = path.abspath(path.dirname(__file__))
# load dotenv from '/home/dron/PycharmProjects/flaskProjects/flask_blog/.env' in our case
load_dotenv(path.join(basedir, '.env'))


class Config(object):
    """Set Flask config variables."""
    SECRET_KEY = environ.get('SECRET_KEY')

    # Database
    SQLALCHEMY_DATABASE_URI = 'postgresql://dron_test:2805@localhost/tim_proj'

    # Recaptcha
    RECAPTCHA_PUBLIC_KEY = '6LfDe1gkAAAAAJ1VpcKubUCtmHz2rMMYFO5i51Ng'
    RECAPTCHA_PRIVATE_KEY = '6LfDe1gkAAAAAMlKVfQT1qcVJRhZLdlekY0CTCW2'
    RECAPTCHA_OPTIONS = {'theme': 'black'}


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    DEBUG = True
    # For UNIT tests
    # TESTING = True
