import os
from flask import Blueprint, jsonify, send_from_directory, request, Response
from werkzeug.utils import secure_filename
from flask_restful import Resource


main_blueprint = Blueprint('main', __name__)


class StaticFolder(Resource):
    def __init__(self, **kwargs) -> None:
       self.filename = kwargs['filename']

    def get(self) -> Response:
        return send_from_directory(main_blueprint.config['STATIC_FOLDER'], self.filename)


# TODO: change this

@main_blueprint.route('/media/<path:filename>')
def mediafiles(filename):
    return send_from_directory(main_blueprint.config['MEDIA_FOLDER'], filename)


@main_blueprint.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(main_blueprint.config['MEDIA_FOLDER'], filename))
    return '''
    <!doctype html>
    <title>upload new File</title>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file><input type=submit value=Upload>
    </form>
    '''
