from os import path, listdir

from flask import render_template, Flask, abort
from jinja2.exceptions import TemplateNotFound


def bind_html(app: Flask):
    @app.route('/')
    @app.route('/index.html')
    def index():
        try:
            return render_template("index.html")
        except TemplateNotFound:
            return abort(404)

    @app.route('/<string:dir_name>')
    @app.route('/<string:dir_name>/<string:file_name>')
    def directory(dir_name: str, file_name: str = 'index.html'):
        if dir_name == 'admin':
            return abort(404)
        dir_name_full = path.join(
            app.template_folder[3:] if app.template_folder.startswith('../') else app.template_folder, dir_name
        )
        if path.isdir(dir_name_full):
            files = {i for i in listdir(dir_name_full) if i.endswith('.htm') or i.endswith('.html')}
            if file_name in files:
                template_name = path.join(dir_name, file_name)
            elif files and file_name == "index.html":
                template_name = path.join(dir_name, files.pop())
            else:
                return abort(404)
        else:
            return abort(404)
        try:
            return render_template(template_name)
        except TemplateNotFound:
            return abort(404)
