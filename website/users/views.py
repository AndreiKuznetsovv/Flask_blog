import os

from flask import (
    Blueprint, render_template,
    redirect, url_for,
    flash, request,
    current_app,
)
from flask_login import (
    login_user, logout_user,
    login_required, current_user,
)
from werkzeug.security import (
    generate_password_hash, check_password_hash,
)

from website.models import (
    UserInfo, db_add_func,
    db_commit_func, Post,
)
from website.utils import save_image, send_reset_email
from .forms import (
    RegistrationForm, LoginForm,
    RequestResetForm, ResetPasswordForm,
    UpdateAccountForm,
)

users = Blueprint('users', __name__)


@users.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateAccountForm()

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data

        if form.image.data:
            # saving old user image filename to delete it
            old_image_filename = current_user.image
            image_filename = save_image(form.image.data)
            current_user.image = image_filename

            if db_commit_func():
                # deleting old image if it's not default
                if old_image_filename != 'default.png':
                    os.remove(os.path.join(current_app.root_path, 'static/profile_pics', old_image_filename))
                flash('Account has been updated!', category='success')
                return redirect(url_for('users.profile', username=current_user.username))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename=f'profile_pics/{current_user.image}')
    return render_template("users/profile.html", user=current_user,
                           form=form, image=image_file)


@users.route("/posts/<string:username>")
def user_posts(username: str):
    # check if the requested user exists
    user = UserInfo.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', default=1, type=int)
    posts = Post.query.filter_by(user_id=user.id) \
        .order_by(Post.date_created.desc()) \
        .paginate(page=page, per_page=5)

    if not posts:
        flash('This user has no posts:(', category='error')

    return render_template("users/user_posts.html", user=current_user, username=username, posts=posts)


@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = UserInfo.query.filter_by(email=form.email.data).first()
        if check_password_hash(user.password, form.password.data):
            flash('Logged in!', category='success')
            login_user(user, remember=form.remember.data)
            return redirect(url_for('main.home'))
        else:
            flash('Password is incorrect!', category='error')

    return render_template('users/login.html', user=current_user, form=form)


@users.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = UserInfo(username=form.username.data,
                            email=form.email.data, password=hashed_password)

        if db_add_func(new_user):
            flash('Account created!', category='success')
            login_user(new_user, remember=True)
            return redirect(url_for('main.home'))
        else:
            return redirect(url_for('auth.sign_up'))

    return render_template('users/signup.html', user=current_user, form=form)


# The view for logout from current account
@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.home"))


@users.route('/reset-password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RequestResetForm()
    if form.validate_on_submit():
        user = UserInfo.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instruction to reset your password', category='success')
        return redirect(url_for('.login'))

    return render_template('users/reset_request.html',
                           title='Reset Password', form=form, user=current_user)


@users.route('/reset-password/<string:token>', methods=['GET', 'POST'])
def reset_token(token: str):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = UserInfo.verify_reset_token(token)

    if not user:
        flash('That is token is invalid or expired!', category='error')
        return redirect(url_for('.reset_request'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        user.password = hashed_password
        if db_commit_func():
            flash('Password successfully changed!', category='success')
            login_user(user, remember=True)
            return redirect(url_for('main.home'))

    return render_template('users/reset_token.html',
                           title='Reset Password', form=form, user=current_user)
