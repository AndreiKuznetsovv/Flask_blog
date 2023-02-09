class Config(object):
    SECRET_KEY = "dc64a3eed4ff9c9f7ae9e22c8e597654"  # got it from secrets.token_hex(16)
    SQLALCHEMY_DATABASE_URI = 'postgresql://dron_test:2805@localhost/tim_proj'
    # constants for recaptcha
    RECAPTCHA_PUBLIC_KEY = '6LfDe1gkAAAAAJ1VpcKubUCtmHz2rMMYFO5i51Ng'
    RECAPTCHA_PRIVATE_KEY = '6LfDe1gkAAAAAMlKVfQT1qcVJRhZLdlekY0CTCW2'
    RECAPTCHA_OPTIONS = {'theme': 'black'}
    DEBUG = False
    TESTING = False


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
