from flask import Flask


def create_app():
    # create an app
    app = Flask(__name__)

    # import development config class
    from website.config import DevelopmentConfig
    # load config from config.py file
    app.config.from_object(DevelopmentConfig)

    from .models import (
        UserInfo, Post,
        Comment, Likes,
        db, mail,
        login_manager, migrate,
    )

    db.init_app(app)  # initialize the database
    mail.init_app(app)  # initialize the mail server
    login_manager.init_app(app)  # initialize the login manager
    migrate.init_app(app, db)  # initialize the flask migrate

    # imports for blueprints
    from .main.views import main
    from .posts.views import posts
    from .users.views import users
    from .errors.handlers import errors

    app.register_blueprint(main,
                           url_prefix="/")  # url_prefix if you need this route /prefix/home for /home in views (just example)
    app.register_blueprint(posts, url_prefix="/")
    app.register_blueprint(users, url_prefix="/")
    app.register_blueprint(errors, url_prefix="/")

    # use this to create tables
    # def test_connection():
    #     with app.app_context():
    #         db.create_all()
    # test_connection()

    return app
