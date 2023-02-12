from flask import flash, current_app
from flask_login import UserMixin
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import URLSafeTimedSerializer as Serializer
from itsdangerous.exc import SignatureExpired, BadTimeSignature
from sqlalchemy import exc
from sqlalchemy.sql import func

# db creation
db = SQLAlchemy()

# mail creation
mail = Mail()


# function for adding data to database
def db_add_func(data):
    try:
        db.session.add(data)
        db.session.commit()
        return True
    except exc.SQLAlchemyError:
        flash('A database error occurred during creation', category='error')
        return False


# function for deleting data from database
def db_delete_func(data):
    try:
        db.session.delete(data)
        db.session.commit()
        return True
    except exc.SQLAlchemyError:
        flash('A database error occurred during deletion', category='error')
        return False


# function for commit data to database / using when updating some info
def db_commit_func():
    try:
        db.session.commit()
        return True
    except exc.SQLAlchemyError:
        flash('A database error occurred during deletion', category='error')
        return False


# table for users
class UserInfo(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    image = db.Column(db.String(20), nullable=False, default='default.png')  # users profile image
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())  # func.now gives as the current time
    # one-to-many relationship for users and posts
    posts = db.relationship('Post', backref='user_info', passive_deletes=True, lazy=True)
    # one-to-many relationship for users and comments
    comments = db.relationship('Comment', backref='user_info', passive_deletes=True)
    # one-to-many relationship for users and likes
    likes = db.relationship('Likes', backref='user_info', passive_deletes=True)

    # This token needs to make safe url for reset password
    def get_reset_token(self):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id})

    @staticmethod
    def verify_reset_token(token, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token, max_age=expires_sec)['user_id']
        except (SignatureExpired, BadTimeSignature):
            return None
        return UserInfo.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


# table for posts
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    # foreign key to table UserInfo (user_info in postgres)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user_info.id', ondelete="CASCADE"), nullable=False)
    # one-to-many relationship for posts and comments
    comments = db.relationship('Comment', backref='post', passive_deletes=True)
    # one-to-many relationship for posts and likes
    likes = db.relationship('Likes', backref='post', passive_deletes=True)

    def __repr__(self):
        return f"Post('{self.id}', '{self.user_id}')"


# table for comments
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    # foreign key to table UserInfo (user_info in postgres)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user_info.id', ondelete="CASCADE"), nullable=False)
    # foreign key to table Post (post in postgres)
    post_id = db.Column(db.Integer, db.ForeignKey(
        'post.id', ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        return '<Post %r>' % self.id


# table for likes
class Likes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    # foreign key to table UserInfo (user_info in postgres)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user_info.id', ondelete='CASCADE'), nullable=False)
    # foreign key to table Post (post in postgres)
    post_id = db.Column(db.Integer, db.ForeignKey(
        'post.id', ondelete='CASCADE'), nullable=False)

    def __repr__(self):
        return '<Post %r>' % self.id
