from app import db
from app.models import Notification

def notify(user, message, link):
    notif = Notification(user_id=user.id, message=message, link=link)
    db.session.add(notif)
    db.session.commit()
