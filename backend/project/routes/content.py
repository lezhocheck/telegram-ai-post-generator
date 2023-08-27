from flask import request, Response, Blueprint
from project.services.content import get_user_content
from project.utils.common import login_required
from flask_jwt_extended import get_jwt_identity


content_blueprint = Blueprint('content', __name__)


@content_blueprint.route('/content', methods=['GET'])
@login_required
def get_queries() -> Response:
    user_id = get_jwt_identity()
    return get_user_content(user_id)


@content_blueprint.route('/content/<int:id>', methods=['GET'])
@login_required
def get_query(id: int) -> Response:
    user_id = get_jwt_identity()
    return get_user_content(user_id, id)