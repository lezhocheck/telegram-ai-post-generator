from flask import Response, Blueprint
from project.utils.common import format_response


error_blueprint = Blueprint('error', __name__)


@error_blueprint.errorhandler(Exception) 
def handle_error(error) -> Response:
    return format_response(message=error, status=error.status_code)