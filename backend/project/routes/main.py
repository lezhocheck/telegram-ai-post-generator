import os
from flask import send_from_directory, request, Response, current_app, Blueprint
from werkzeug.utils import secure_filename
from project.utils.common import format_response
from project.utils.codes import HTTP_200_OK


main_blueprint = Blueprint('main', __name__)


@main_blueprint.route('/static/<path:filename>')
def get_static(filename: str) -> Response:
    return send_from_directory(current_app.config['STATIC_FOLDER'], filename)