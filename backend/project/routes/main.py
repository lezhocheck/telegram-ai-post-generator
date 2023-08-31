import os
from flask import send_from_directory, Response, current_app, Blueprint
from project.utils.common import format_response
from project.utils.codes import HTTP_200_OK


main_blueprint = Blueprint('main', __name__)


@main_blueprint.route('/static/<path:filename>')
def get_static(filename: str) -> Response:
    return send_from_directory(current_app.config['STATIC_FOLDER'], filename)