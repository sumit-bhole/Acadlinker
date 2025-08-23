# routes.py - acadlinker/app/groups/
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from app import db
from app.models import User, Group, GroupInvite, group_members
from app.groups.forms import CreateGroupForm
from app.notifications.notify import notify  # ✅ Import notify

groups_bp = Blueprint('groups', __name__, url_prefix='/groups')

@groups_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = CreateGroupForm()
    if form.validate_on_submit():
        group = Group(title=form.title.data, description=form.description.data, creator_id=current_user.id)
        group.members.append(current_user)
        db.session.add(group)
        db.session.commit()
        flash('Group created!', 'success')
        return redirect(url_for('groups.view', group_id=group.id))
    return render_template('groups/create_group.html', form=form)

@groups_bp.route('/view/<int:group_id>')
@login_required
def view(group_id):
    group = Group.query.get_or_404(group_id)
    return render_template('groups/group_detail.html', group=group)

@groups_bp.route('/invite/<int:group_id>/<int:user_id>')
@login_required
def invite(group_id, user_id):
    group = Group.query.get_or_404(group_id)

    if current_user not in group.members:
        flash("Only group members can invite.", "danger")
        return redirect(url_for('groups.view', group_id=group_id))

    if len(group.members) >= 15:
        flash("Group limit reached (15).", "danger")
        return redirect(url_for('groups.view', group_id=group_id))

    friend = User.query.get_or_404(user_id)
    invite = GroupInvite.query.filter_by(group_id=group_id, user_id=user_id).first()
    if invite:
        flash("Already invited.", "info")
    else:
        invite = GroupInvite(group_id=group_id, user_id=user_id)
        db.session.add(invite)
        db.session.commit()

        # ✅ Send notification to invited user
        notify(friend, f"You’ve been invited to join group '{group.title}'.", "/groups/invites")

        flash(f"Invitation sent to {friend.full_name}", "success")
    
    return redirect(url_for('groups.view', group_id=group_id))

@groups_bp.route('/invites')
@login_required
def invites():
    invites = GroupInvite.query.filter_by(user_id=current_user.id, status='pending').all()
    return render_template('groups/group_invites.html', invites=invites)

@groups_bp.route('/accept_invite/<int:invite_id>')
@login_required
def accept_invite(invite_id):
    invite = GroupInvite.query.get_or_404(invite_id)
    group = Group.query.get(invite.group_id)

    if len(group.members) >= 15:
        flash("Group full.", "warning")
        return redirect(url_for('groups.invites'))

    invite.status = 'accepted'
    group.members.append(current_user)
    db.session.commit()

    # ✅ Notify group creator
    creator = User.query.get(group.creator_id)
    notify(creator, f"{current_user.full_name} joined your group '{group.title}'.", f"/groups/view/{group.id}")

    flash("Joined group!", "success")
    return redirect(url_for('groups.view', group_id=group.id))

@groups_bp.route('/reject_invite/<int:invite_id>')
@login_required
def reject_invite(invite_id):
    invite = GroupInvite.query.get_or_404(invite_id)
    invite.status = 'rejected'
    db.session.commit()

    # ✅ Notify group creator
    group = Group.query.get(invite.group_id)
    creator = User.query.get(group.creator_id)
    notify(creator, f"{current_user.full_name} rejected your invite to '{group.title}'.", f"/groups/view/{group.id}")

    flash("Invitation declined.", "info")
    return redirect(url_for('groups.invites'))
