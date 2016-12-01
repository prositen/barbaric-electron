from ipaddress import ip_address

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
from app.models.file import DirectoryForm, Directory


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
        print(directory.id)
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
