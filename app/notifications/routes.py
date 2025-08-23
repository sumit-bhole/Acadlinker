# routes.py - placeholder for acadlinker/app/notifications/
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app import db
from app.models import Notification

notifications_bp = Blueprint('notifications', __name__, url_prefix='/notifications')

@notifications_bp.route('/')
@login_required
def all():
    notifications = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.timestamp.desc()).all()

    # Mark all as read
    for n in notifications:
        if not n.is_read:
            n.is_read = True
    db.session.commit()

    return render_template('notifications/all.html', notifications=notifications)
