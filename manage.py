#!/usr/bin/env python
import os

import flask_security
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import getpass
import binascii

from app import db, app, user_datastore

migrate = Migrate(app, db)
manager = Manager(app)


@manager.command
def add_admin(email):
    """ Creates an admin user and adds it to the database """
    pwd = getpass.getpass("Password for " + email + ": ")
    verify = getpass.getpass("Verify password for " + email + ": ")
    if pwd != verify:
        print("Passwords don't match")
        return
    salt = binascii.hexlify(os.urandom(32))
    encrypted_pwd = flask_security.utils.encrypt_password(password=pwd)

    admin = user_datastore.create_user(email=email, password=encrypted_pwd)
    user_datastore.add_role_to_user(admin, 'Admin')
    user_datastore.commit()


manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
