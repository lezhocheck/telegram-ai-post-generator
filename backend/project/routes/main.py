import os
from flask import send_from_directory, Response, current_app, Blueprint
from project.utils.error import BadRequest


main_blueprint = Blueprint('main', __name__)


def find_file_by_name(dir: str, name: str) -> str:
    result = None
    for _, _, files in os.walk(dir):
        fs = [os.path.splitext(f)[0] for f in files]
        try:
            idx = fs.index(name)
            result = files[idx]
        except ValueError:
            pass
    if not result:
        raise BadRequest('Invalid filename')
    return result


@main_blueprint.route('/static/<string:name>')
def get_from_static(name: str) -> Response:
    static_dir = current_app.config['STATIC_FOLDER']
    file = find_file_by_name(static_dir, name)
    return send_from_directory(static_dir, file)