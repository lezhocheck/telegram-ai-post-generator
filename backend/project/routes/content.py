from flask import Response, Blueprint
from project.services.content import get_content, get_content_by_id
from project.services.user import login_required
from project.models.user import User
from project.utils.format import response


content_blueprint = Blueprint('content', __name__)


@content_blueprint.route('/content', methods=['GET'])
@login_required
def select_contents(user: User) -> Response:
    data, code = get_content(user)
    return response(data, code)


@content_blueprint.route('/content/<int:id>', methods=['GET'])
@login_required
def select_content(user: User, id: int) -> Response:
    data, code = get_content_by_id(user, id)
    return response(data, code)
