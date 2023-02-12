import json

from flask import (
    render_template,
    flash,
    redirect, url_for,
    Blueprint, abort,
    request, jsonify,
)
from flask_login import (
    login_required, current_user,
)
from sqlalchemy import exc

from website.models import (
    Post, db_add_func,
    db_delete_func, db_commit_func,
    db, Likes,
    Comment,
)
from .forms import PostForm

posts = Blueprint('posts', __name__)


@posts.route('/create-post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        new_post = Post(title=form.title.data, text=form.content.data, user_id=current_user.id)
        if db_add_func(new_post):
            flash('Post created!', category='success')
        return redirect(url_for('main.home'))

    return render_template('posts/create_post.html', user=current_user,
                           form=form, legend='New post')


# The view for deleting post if current user are owner
@posts.route("/delete-post/<int:post_id>", methods=['POST'])
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
    return redirect(url_for('main.home'))


@posts.route("/update-post/<int:post_id>", methods=['GET', 'POST'])
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
                return redirect(url_for('main.home'))
        elif request.method == 'GET':
            form.title.data = post.title
            form.content.data = post.text

    return render_template('posts/edit_post.html', user=current_user, legend='Edit your post', form=form)


@posts.route('/create-many-posts', methods=['GET', 'POST'])
@login_required
def create_many_posts():
    with open('data.json', 'r') as in_data:
        json_data = json.load(in_data)

    for post_data in json_data:
        title = post_data['title']
        content = post_data['content']
        user_id = post_data['user_id']
        new_post = Post(title=title, text=content, user_id=user_id)
        db_add_func(new_post)
    return redirect(url_for('main.home'))


'''Likes and comments'''


# The view for leaving comments below the post
@posts.route("/create-comment/<int:post_id>", methods=['GET', 'POST'])
@login_required
def create_comment(post_id: int):
    if request.method == 'POST':
        text = request.form.get('text')

        if not text:
            flash('Comment cannot be empty', category='error')
            return redirect(url_for('main.home'))
        else:
            post = Post.query.filter_by(id=post_id).first()
            if post:
                comment = Comment(text=text, user_id=current_user.id, post_id=post_id)
                db_add_func(comment)
            else:
                flash('Post does not exist', category='error')

    return redirect(url_for('main.home'))


# The view for deleting comment if current user are owner of the comment OR owner of the post
@posts.route("/delete-comment/<int:comment_id>")
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
    return redirect(url_for('main.home'))


@posts.route("/like-post/<int:post_id>", methods=['GET', 'POST'])
@login_required
def like(post_id: int):
    post = Post.query.filter_by(id=post_id).first()
    like = Likes.query.filter_by(user_id=current_user.id, post_id=post.id).first()

    if not post:
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
