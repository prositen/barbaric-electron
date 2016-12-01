
from app import db
from app.models import ModelForm


class File(db.Model):
    name = db.Column(db.String(255), primary_key=True)
    description = db.Column(db.Text())
    directory_id = db.Column(db.Integer, db.ForeignKey('directory.id'))


class Directory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), index=True, unique=True, info={'label': 'Display name'})
    path = db.Column(db.String(4096), info={'label': 'File system path'})
    description = db.Column(db.Text())
    files = db.relationship("File", backref='directory')

    @staticmethod
    def get_by_name(name):
        return Directory.query.filter_by(name=name).first()


class DirectoryForm(ModelForm):
    class Meta:
        model = Directory