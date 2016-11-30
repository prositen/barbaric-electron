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
        return Entry.query.filter_by(user_id=user_id)

    @staticmethod
    def get_all():
        return Entry.query.all()

    def get_ip(self):
        return ".".join(map(lambda n: str(self.ip >> n & 0xFF), [24, 16, 8, 0]))