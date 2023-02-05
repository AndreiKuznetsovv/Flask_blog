from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
)

from .models import UserInfo, db_add_func
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import RegistrationForm, LoginForm

# registry blueprint named auth
auth = Blueprint("auth", __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = UserInfo.query.filter_by(email=form.email.data).first()
        if check_password_hash(user.password, form.password.data):
            flash('Logged in!', category='success')
            login_user(user, remember=form.remember.data)
            return redirect(url_for('views.home'))
        else:
            flash('Password is incorrect!', category='error')

    return render_template('login.html', user=current_user, form=form)


@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = UserInfo(username=form.username.data,
                            email=form.email.data, password=hashed_password)

        if db_add_func(new_user):
            flash('Account created!', category='success')
            login_user(new_user, remember=True)
            return redirect(url_for('views.home'))
        else:
            return redirect(url_for('auth.sign_up'))

    return render_template('signup.html', user=current_user, form=form)


# The view for logout from current account
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.home"))
