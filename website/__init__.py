from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


# error handler for 404
def page_not_found(e):
    return render_template('error_404.html'), 404

#error handler for 500
def internal_server_error(e):
    return render_template('error_500.html'), 500

#error handler for 403
def forbidden_error(e):
    return render_template('error_403.html'), 403

def create_app():
    # create an app
    app = Flask(__name__)
    # config secret key and database uri
    app.config['SECRET_KEY'] = "dc64a3eed4ff9c9f7ae9e22c8e597654" # got it from secrets.token_hex(16)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://dron_test:2805@localhost/tim_proj'

    from .models import UserInfo, Post, Comment, Likes, db

    db.init_app(app)  # initialize the database

    # import for handle errors
    from werkzeug.exceptions import NotFound, InternalServerError, Forbidden
    #register error handlers
    app.register_error_handler(NotFound, page_not_found) # status code 404
    app.register_error_handler(InternalServerError, internal_server_error) # status code 500
    app.register_error_handler(Forbidden, forbidden_error) # status code 403

    #imports for blueprints
    from .views import views
    from .auth import auth

    app.register_blueprint(views,
                           url_prefix="/")  # url_prefix if you need this route /prefix/home for /home in views (just example)
    app.register_blueprint(auth, url_prefix="/")

    # use this to create tables
    # def test_connection():
    #     with app.app_context():
    #         db.create_all()
    # test_connection()

    # creating login manager
    login_manager = LoginManager()
    # for redirection users to auth view
    login_manager.login_view = "auth.login"
    # init login manager
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        # get id from session,then retrieve user object from database with peewee query
        return UserInfo.query.get(int(id))

    return app
