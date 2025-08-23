from flask import Blueprint, redirect, url_for, flash, request, render_template
from flask_login import login_required, current_user
from app import db
from app.models import User, FriendRequest
from app.notifications.notify import notify  # ✅ Import notify function

friends_bp = Blueprint('friends', __name__, url_prefix='/friends')

@friends_bp.route('/send/<int:user_id>',methods=['POST'])
@login_required
def send_request(user_id):
    target_user = User.query.get_or_404(user_id)

    if target_user == current_user:
        flash("You can't send a friend request to yourself!", "warning")
        return redirect(url_for('profile.view',user_id=target_user.id))

    # Check if already friends or request exists
    if current_user.friends.filter_by(id=target_user.id).first():
        flash("Already friends!", "info")
    elif FriendRequest.query.filter_by(sender_id=current_user.id, receiver_id=target_user.id).first():
        flash("Friend request already sent!", "info")
    else:
        req = FriendRequest(sender_id=current_user.id, receiver_id=target_user.id)
        db.session.add(req)
        db.session.commit()

        # ✅ Send notification
        notify(
            target_user,
            f"{current_user.full_name} sent you a friend request.",
            "/friends/requests"
        )

        flash("Friend request sent!", "success")

    return redirect(url_for('profile.view', user_id=target_user.id))

@friends_bp.route('/requests')
@login_required
def requests():
    pending = FriendRequest.query.filter_by(receiver_id=current_user.id, status='pending').all()
    return render_template('friends/requests.html', requests=pending)

@friends_bp.route('/accept/<int:req_id>')
@login_required
def accept(req_id):
    req = FriendRequest.query.get_or_404(req_id)
    if req.receiver != current_user:
        flash("Unauthorized!", "danger")
        return redirect(url_for('friends.requests'))

    req.status = 'accepted'
    current_user.friends.append(req.sender)
    req.sender.friends.append(current_user)
    db.session.commit()

    # ✅ Notify sender
    notify(
        req.sender,
        f"{current_user.full_name} accepted your friend request.",
        "/friends/list"
    )

    flash("Friend request accepted!", "success")
    return redirect(url_for('friends.requests'))

@friends_bp.route('/reject/<int:req_id>')
@login_required
def reject(req_id):
    req = FriendRequest.query.get_or_404(req_id)
    if req.receiver != current_user:
        flash("Unauthorized!", "danger")
        return redirect(url_for('friends.requests'))

    req.status = 'rejected'
    db.session.commit()
    flash("Friend request rejected!", "info")
    return redirect(url_for('friends.requests'))

@friends_bp.route('/list')
@login_required
def list_friends():
    friends = current_user.friends.all()
    return render_template('friends/list.html', friends=friends)

@friends_bp.route('/search', methods=['GET', 'POST'])
@login_required
def search_friends():
    query = request.args.get('q', '')
    results = []

    if query:
        results = User.query.filter(
            User.id != current_user.id,
            User.skills.ilike(f'%{query}%')
        ).all()

    return render_template('friends/search_friends.html', results=results, query=query)
