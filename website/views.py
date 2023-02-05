import secrets
import os
from PIL import Image
from flask import (
    Blueprint, render_template,
    request, flash,
    redirect, url_for,
    jsonify, abort,
)
from flask_login import login_required, current_user
from sqlalchemy import exc
from .models import (
    UserInfo, Post,
    Comment, Likes,
    db, db_add_func,
    db_delete_func,
    db_commit_func,
)
from .forms import PostForm, UpdateAccountForm, CommentForm

views = Blueprint("views", __name__)


@views.route('/')
@views.route('/home')
@login_required
def home():
    page = request.args.get('page', default=1, type=int)
    posts = Post.query.order_by(Post.date_created.desc()).paginate(page=page, per_page=5)
    return render_template("home.html", user=current_user, posts=posts)


@views.route('/create-post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        new_post = Post(title=form.title.data, text=form.content.data, user_id=current_user.id)
        if db_add_func(new_post):
            flash('Post created!', category='success')
        return redirect(url_for('.home'))

    return render_template('create_post.html', user=current_user,
                           form=form, legend='New post')


# The view for deleting post if current user are owner
@views.route("/delete-post/<int:post_id>", methods=['POST'])
@login_required
def delete_post(post_id: int):
    post = Post.query.filter_by(id=post_id).first()

    if not post:
        flash('Post does not exist', category='error')
    elif current_user.id != post.user_id:
        flash('You do not have permission to delete this post', category='error')
    else:
        if db_delete_func(post):
            flash('Post deleted!', category='success')
    return redirect(url_for('.home'))


# function for saving picture in profile endpoint
def save_image(form_image):
    # creating a random hex value for image name
    random_hex = secrets.token_hex(8)
    # get the filename and the extension of the user image
    _, f_ext = os.path.splitext(form_image.filename)
    image_filename = random_hex + f_ext
    image_path = os.path.join(views.root_path, 'static/profile_pics', image_filename)
    # resize image
    output_size = (125, 125)
    resize_image = Image.open(form_image)
    resize_image.thumbnail(output_size)
    # save our image
    resize_image.save(image_path)
    return image_filename


# The view for showing up all posts for chosen user
@views.route("/profile", methods=['GET', 'POST'])
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
                    os.remove(os.path.join(views.root_path, 'static/profile_pics', old_image_filename))
                flash('Account has been updated!', category='success')
                return redirect(url_for('views.profile', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename=f'profile_pics/{current_user.image}')

    return render_template("profile.html", user=current_user,
                           form=form, image=image_file)


@views.route("/posts/<string:username>")
def user_posts(username: str):
    # check if the requested user exists
    user = UserInfo.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', default=1, type=int)
    posts = Post.query.filter_by(user_id=user.id) \
        .order_by(Post.date_created.desc()) \
        .paginate(page=page, per_page=5)

    if not posts:
        flash('This user has no posts:(', category='error')

    return render_template("user_posts.html", user=current_user, username=username, posts=posts)


# The view for leaving comments below the post
@views.route("/create-comment/<int:post_id>", methods=['GET', 'POST'])
@login_required
def create_comment(post_id: int):
    if request.method == 'POST':
        text = request.form.get('text')
        # new commit
        if not text:
            flash('Comment cannot be empty', category='error')
            return redirect(url_for('.home'))
        else:
            post = Post.query.filter_by(id=post_id).first()
            if post:
                comment = Comment(text=text, user_id=current_user.id, post_id=post_id)
                db_add_func(comment)
            else:
                flash('Post does not exist', category='error')

    return redirect(url_for('.home'))
    # form = CommentForm()
    #
    # if form.validate_on_submit():
    #     post = Post.query.filter_by(id=post_id).first()
    #     if post:
    #         comment = Comment(text=form.content, user_id=current_user.id, post_id=post_id)
    #         db_add_func(comment)
    #     else:
    #         flash('POst does not exist', category='error')
    #
    # return render_template('home.html', form=form, user=current_user)


# The view for deleting comment if current user are owner of the comment OR owner of the post
@views.route("/delete-comment/<int:comment_id>")
@login_required
def delete_comment(comment_id: int):
    comment = Comment.query.filter_by(id=comment_id).first()

    if not comment:
        flash('Comment does not exist', category='error')
    elif (current_user.id != comment.user_id) and \
            (current_user.id != comment.post.user_id):
        flash('You do not have permission to delete this comment', category='error')
    else:
        db_delete_func(comment)
    return redirect(url_for('.home'))


@views.route("/like-post/<int:post_id>", methods=['GET', 'POST'])
@login_required
def like(post_id: int):
    post = Post.query.filter_by(id=post_id).first()
    like = Likes.query.filter_by(user_id=current_user.id, post_id=post.id).first()

    if not post:
        # flash('Post does not exist', category='error')
        return jsonify({'error': 'Post does not exist'}, 400)
    elif like:
        try:
            db.session.delete(like)
            db.session.commit()
        except exc.SQLAlchemyError:
            flash('An database error occurred during deletion', category='error')
    else:
        new_like = Likes(user_id=current_user.id, post_id=post_id)
        try:
            db.session.add(new_like)
            db.session.commit()
        except exc.SQLAlchemyError:
            flash('An database error occurred during creation', category='error')
    return jsonify({"likes": len(post.likes), "liked": current_user.id in map(lambda x: x.user_id, post.likes)})
    # return redirect(url_for('.home'))


@views.route("/update-post/<int:post_id>", methods=['GET', 'POST'])
@login_required
def edit_post(post_id: int):
    form = PostForm()
    post = Post.query.get_or_404(post_id)

    if not post.user_id == current_user.id:
        abort(403)
    else:
        if form.validate_on_submit():
            post.text = form.content.data

            if db_commit_func():
                flash('Information Updated!', category='success')
                return redirect(url_for('.home'))
        elif request.method == 'GET':
            form.content.data = post.text

    return render_template('create_post.html', user=current_user, legend='Edit your post', form=form)
