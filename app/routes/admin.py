from ipaddress import ip_address
from pathlib import Path

from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_security import roles_accepted
from flask_login import current_user
from werkzeug.exceptions import NotFound

from app import Entry
from app import app, db
from app.models.file import DirectoryForm, Directory, FileForm, File


def get_file_and_directory(name):
    try:
        path, name = name.rsplit('/', 1)
    except ValueError:
        raise NotFound

    directory = Directory.get_by_name(path)
    if not directory:
        raise NotFound

    p = Path(directory.path + '/' + name)
    if not p.is_file():
        raise NotFound
    return directory, p, name


@app.route('/admin/directory/add', methods=['GET', 'POST'])
@roles_accepted('Admin')
def admin_directory_add():
    form = DirectoryForm()
    directory = Directory()
    if form.validate_on_submit():

        form.populate_obj(directory)
        db.session.add(directory)
        db.session.flush()
        directory.save()
        entry = Entry(user_id=current_user.id, ip=int(ip_address(request.remote_addr)),
                      message="Added directory {0}, {1}".format(directory.id, directory.path))
        entry.save()
        db.session.add(entry)
        db.session.commit()
        flash(u"Directory added", 'success')
        return redirect(url_for('index'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(u"Error in %s - %s" % (getattr(form, field).label.text, error), 'error')
        return render_template('add_directory.html.j2', form=form)


@app.route('/admin/directory/edit/<path:name>', methods=['GET'])
@roles_accepted('Admin')
def admin_show_directory_edit(name):
    directory = Directory.get_by_name(name)
    if directory:
        form = DirectoryForm(obj=directory)
        return render_template('edit_directory.html.j2', form=form, directory_id=directory.id)
    else:
        raise NotFound


@app.route('/admin/directory/edit', methods=['POST'])
@roles_accepted('Admin')
def admin_directory_edit():
    directory_id = request.form.get('directory_id')
    directory = Directory.query.get(directory_id)
    old_path = directory.path
    old_name = directory.name
    old_description = directory.description

    if not directory:
        raise NotFound
    form = DirectoryForm(obj=directory)
    form.populate_obj(directory)
    if form.validate_on_submit():
        message = Entry.make_diff_message({"File system path": (old_path, directory.path),
                                           "Display name": (old_name, directory.name),
                                           "Description": (old_description, directory.description)})
        entry = Entry(user_id=current_user.id,
                      ip=int(ip_address(request.remote_addr)),
                      message="Edited directory {0}, {1}".format(directory_id, message))

        db.session.add(entry)
        db.session.commit()
        flash(u"Directory added", 'success')
        return redirect(url_for('index'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(u"Error in %s - %s" % (getattr(form, field).label.text, error), 'error')
        return render_template('add_directory.html.j2', form=form,
                               header="Add directory",
                               action="admin_directory_add")


@app.route('/admin/file/edit/<path:name>', methods=['GET'])
@roles_accepted('Admin')
def admin_show_file_edit(name):
    directory, file, name = get_file_and_directory(name)
    file = File.get_by_directory_and_name(directory, name)
    form = FileForm(obj=file)
    return render_template('edit_file.html.j2', form=form, name=name, directory_id=directory.id)


@app.route('/admin/file/edit', methods=['POST'])
@roles_accepted('Admin')
def admin_file_edit():
    directory_id = request.form.get('directory_id')
    directory = Directory.query.get(directory_id)

    name = request.form.get('name')
    file = File.get_by_directory_and_name(directory, name)
    if file:
        old_description = file.description
    else:
        p = Path(directory.path + '/' + name)
        if not p.is_file():
            raise NotFound
        file = File(name=name, directory_id=directory.id)
        db.session.add(file)
        old_description = "No description"

    form = FileForm(obj=file)
    if form.validate_on_submit():
        form.populate_obj(file)
        message = Entry.make_diff_message({"Description": (old_description, file.description)})
        entry = Entry(user_id=current_user.id,
                      ip=int(ip_address(request.remote_addr)),
                      message="Edited file {0}, {1}".format(directory.path + '/' + file.name, message))

        db.session.add(entry)
        db.session.commit()
        flash(u"File edited", 'success')
        return redirect(url_for('browse_path', name=directory.name))
