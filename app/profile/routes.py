import os
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app import db
from app.profile.forms import EditProfileForm
from app.models import User,Post

profile_bp = Blueprint('profile', __name__, url_prefix='/profile')

UPLOAD_FOLDER = 'app/static/uploads'

@profile_bp.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    form = EditProfileForm(obj=current_user)

    if form.validate_on_submit():
        current_user.full_name = form.full_name.data
        current_user.email = form.email.data
        current_user.mobile_no = form.mobile_no.data
        current_user.location = form.location.data
        current_user.description = form.description.data
        current_user.skills = form.skills.data
        current_user.education = form.education.data

        if form.profile_pic.data:
            filename = secure_filename(form.profile_pic.data.filename)
            path = os.path.join(UPLOAD_FOLDER, filename)
            form.profile_pic.data.save(path)
            current_user.profile_pic = filename

        if form.cover_photo.data:
            filename = secure_filename(form.cover_photo.data.filename)
            path = os.path.join(UPLOAD_FOLDER, filename)
            form.cover_photo.data.save(path)
            current_user.cover_photo = filename

        db.session.commit()
        flash("Profile updated!", "success")
        return redirect(url_for('profile.view', user_id=current_user.id))

    return render_template('profile/edit_profile.html', form=form)

@profile_bp.route('/<int:user_id>')
@login_required
def view(user_id):
    user = User.query.get_or_404(user_id)

     # Check if the current user is viewing their own profile or a friend's
    is_friend = user in current_user.friends

    if current_user.id == user.id or is_friend:
        user_posts = Post.query.filter_by(user_id=user.id).order_by(Post.timestamp.desc()).all()
    else:
        user_posts = []  # Don't show posts if not self or friend
        
    return render_template('profile/view_profile.html', user=user,user_posts=user_posts)
