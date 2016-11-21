from app import db
from flask_security import UserMixin, RoleMixin

roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id'), primary_key=True),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id'), primary_key=True))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String)
    authenticated = db.Column(db.Boolean, default=False)
    active = db.Column(db.Boolean)
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    @staticmethod
    def get_all():
        return User.query.all()

    def get_email(self, is_admin):
        if is_admin:
            return self.email
        else:
            at_sign = self.email.find('@')
            last_dot = self.email.rfind('.')
            if at_sign and last_dot:
                return self.email[:at_sign + 1] + '********' + self.email[last_dot:]
