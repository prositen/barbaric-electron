import os
from flask import Flask
from flask_jsglue import JSGlue
from flask_login import LoginManager
from flask_security import SQLAlchemyUserDatastore, Security
from flask_sqlalchemy import SQLAlchemy
from config import basedir
from app import custom_filters

app = Flask(__name__,
            template_folder=os.path.join(basedir, 'app', 'templates'),
            static_folder=os.path.join(basedir, 'app', 'static'))
app.config.from_object('config')
app.register_blueprint(custom_filters.blueprint)

jsglue = JSGlue(app)

login_manager = LoginManager()
login_manager.init_app(app)
db = SQLAlchemy(app)


from app.models.user import User, Role
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

from app.models.file import File, Directory
from app.models.audit import Entry

from app.routes.user import *
from app.routes.browse import *
from app.routes.admin import *
