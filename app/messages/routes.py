# routes.py - placeholder for acadlinker/app/messages/
import os
import secrets
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import User, Message
from app import db

messages_bp = Blueprint('messages', __name__, url_prefix='/messages')

UPLOAD_FOLDER = 'app/static/uploads'

def save_file(file):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(file.filename)
    filename = random_hex + f_ext
    path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(path)
    return filename

@messages_bp.route('/chat/<int:user_id>', methods=['GET', 'POST'])
@login_required
def chat(user_id):
    friend = User.query.get_or_404(user_id)
    
    # Must be friends
    if not current_user.friends.filter_by(id=friend.id).first():
        flash("You can only chat with your friends.", "danger")
        return redirect(url_for('user.profile'))

    from app.messages.forms import MessageForm
    form = MessageForm()

    if form.validate_on_submit():
        file_name = None
        if form.file.data:
            file_name = save_file(form.file.data)
        
        msg = Message(
            sender_id=current_user.id,
            receiver_id=friend.id,
            content=form.content.data,
            file_name=file_name
        )
        db.session.add(msg)
        db.session.commit()
        return redirect(url_for('messages.chat', user_id=friend.id))

    # Fetch messages between current_user and friend
    msgs = Message.query.filter(
        ((Message.sender_id == current_user.id) & (Message.receiver_id == friend.id)) |
        ((Message.sender_id == friend.id) & (Message.receiver_id == current_user.id))
    ).order_by(Message.timestamp.asc()).all()

    return render_template('messages/chat.html', form=form, friend=friend, messages=msgs)
