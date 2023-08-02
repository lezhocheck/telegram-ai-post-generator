import os
from flask import Flask, jsonify, send_from_directory, request
from werkzeug.utils import secure_filename
from .extensions import db, swaggerui_blueprint


def register_blueprints(app: Flask):
    app.register_blueprint(swaggerui_blueprint)


def create_app():
    app = Flask(__name__)
    app.config.from_object('project.config.Config')
    db.init_app(app)
    register_blueprints(app)
    return app


app = create_app()


@app.route('/')
def hello_world():
    return jsonify(hello='world')


@app.route('/static/<path:filename>')
def staticfiles(filename):
    return send_from_directory(app.config['STATIC_FOLDER'], filename)


@app.route('/media/<path:filename>')
def mediafiles(filename):
    return send_from_directory(app.config['MEDIA_FOLDER'], filename)


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['MEDIA_FOLDER'], filename))
    return '''
    <!doctype html>
    <title>upload new File</title>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file><input type=submit value=Upload>
    </form>
    '''
