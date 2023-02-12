from flask import Flask
from flask_login import LoginManager


def create_app():
    # create an app
    app = Flask(__name__)

    # import development config class
    from website.config import DevelopmentConfig
    # load config from config.py file
    app.config.from_object(DevelopmentConfig)

    from .models import UserInfo, Post, Comment, Likes, db, mail

    db.init_app(app)  # initialize the database
    mail.init_app(app)  # initialize the mail server

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

    # creating login manager
    login_manager = LoginManager()
    # for redirection users to auth view
    login_manager.login_view = "users.login"
    # init login manager
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        # get id from session,then retrieve user object from database with peewee query
        return UserInfo.query.get(int(id))

    return app
