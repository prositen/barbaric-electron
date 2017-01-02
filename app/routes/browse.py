from pathlib import Path
from flask import render_template
from flask import send_from_directory
from werkzeug.exceptions import NotFound

from app import Directory
from app import File
from app import app


@app.route('/')
def index():
    dirs = Directory.query.all()
    return render_template('index.html.j2',
                           directories=dirs)


@app.route('/browse/<path:name>')
def browse_path(name):
    directory = Directory.get_by_name(name)
    if not directory:
        raise NotFound
    else:
        files = []
        p = Path(directory.path)
        for f in p.iterdir():
            if f.is_file():
                files.append(File.get_file_info(directory, f))
        return render_template('directory.html.j2',
                               path=name, description=directory.description,
                               files=files)


@app.route('/download/<path:name>')
def download(name):
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

    return send_from_directory(directory.path, name)
