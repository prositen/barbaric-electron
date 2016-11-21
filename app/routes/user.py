from flask import render_template
from flask_login import current_user, login_required

from app import Entry
from app import login_manager, app
from app.models.user import User


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/user/profile/<int:user_id>')
def user_profile(user_id):
    user = load_user(user_id)
    audit_entries = []
    if is_admin():
        audit_entries = Entry.get_by_user(user_id)
    return render_template('user.html.j2', user=user, audit_entries=audit_entries)


@app.route('/user/me')
@login_required
def user_me():
    return user_profile(current_user.get_id())


def is_admin():
    return current_user.has_role('Admin')


def yes_no(b):
    if b:
        return "Yes"
    else:
        return "No"


@app.route('/user')
def user():
    raw_users = User.get_all()
    users = list()
    for raw_user in raw_users:
        email = raw_user.get_email()
        admin = yes_no(raw_user.has_role('Admin'))
        users.append({'email': email, 'admin': admin})
    return render_template('users.html.j2', users=users)
