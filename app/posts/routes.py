# routes.py - placeholder for acadlinker/app/posts/
import os
import secrets
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Post
from app.posts.forms import PostForm
from app.notifications.notify import notify

posts_bp = Blueprint('posts', __name__, url_prefix='/posts')

UPLOAD_FOLDER = 'app/static/uploads'

def save_post_file(file):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(file.filename)
    filename = random_hex + f_ext
    path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(path)
    return filename

@posts_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        file_name = None
        if form.file.data:
            file_name = save_post_file(form.file.data)
        post = Post(
            user_id=current_user.id,
            title=form.title.data,
            description=form.description.data,
            file_name=file_name
        )
        db.session.add(post)
        db.session.commit()
        flash("Post created!", "success")
        return redirect(url_for('posts.user_posts'))
    return render_template('posts/create_post.html', form=form)

@posts_bp.route('/my')
@login_required
def user_posts():
    posts = Post.query.filter_by(user_id=current_user.id).order_by(Post.timestamp.desc()).all()
    return render_template('posts/user_posts.html', posts=posts)

@posts_bp.route('/home')
@login_required
def home_feed():
    friend_ids = [f.id for f in current_user.friends]
    posts = Post.query.filter(Post.user_id.in_(friend_ids)).order_by(Post.timestamp.desc()).all()
    return render_template('posts/home_feed.html', posts=posts)
