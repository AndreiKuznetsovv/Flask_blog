from flask import (
    render_template,
    Blueprint, request,
)
from flask_login import (
    login_required, current_user,
)

from website.models import (
    Post, )

main = Blueprint('main', __name__) #template_folder='website/templates'


@main.route('/')
@main.route('/home')
@login_required
def home():
    page = request.args.get('page', default=1, type=int)
    posts = Post.query.order_by(Post.date_created.desc()).paginate(page=page, per_page=5)
    return render_template("main/home.html", user=current_user, posts=posts)


@main.route('/about', methods=['GET'])
def about():
    return render_template('main/about.html')
