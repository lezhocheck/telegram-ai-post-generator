import os
from flask import send_from_directory, request, Response, current_app, Blueprint
from werkzeug.utils import secure_filename
from project.utils.common import format_response
from project.utils.codes import HTTP_200_OK


main_blueprint = Blueprint('main', __name__)


@main_blueprint.route('/static/<path:filename>')
def get_static(filename: str) -> Response:
    return send_from_directory(current_app.config['STATIC_FOLDER'], filename)


@main_blueprint.route('/upload/<path:filename>')
def get_mediafile(filename: str) -> Response:
    return send_from_directory(current_app.config['MEDIA_FOLDER'], filename)


@main_blueprint.route('/upload', methods=['POST'])
def upload_mediafile() -> Response:
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(os.path.join(current_app.config['MEDIA_FOLDER'], filename))
    return format_response(message='Successfully uploaded file', status=HTTP_200_OK)
