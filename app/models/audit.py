from ipaddress import ip_address

from sqlalchemy import func
from app import db


class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=func.now(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    ip = db.Column(db.Integer)
    message = db.Column(db.Text())

    @staticmethod
    def get_by_user(user_id):
        return Entry.query.filter_by(user_id=user_id).order_by(Entry.timestamp.desc())

    @staticmethod
    def get_all():
        return Entry.query.all()

    def get_ip(self):
        return ip_address(self.ip)

    @staticmethod
    def make_diff_message(diff):
        _message = ""
        for header, (old, current) in diff.items():
            _message += "{0}: {1}".format(header, current)
            if old != current:
                _message += "(was {0}), ".format(old)
        return _message
