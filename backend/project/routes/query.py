from flask import request, Response, Blueprint
from project.services import create_query, get_user_querries
from project.utils.common import login_required
from flask_jwt_extended import get_jwt_identity


query_blueprint = Blueprint('query', __name__)


@query_blueprint.route('/query', methods=['POST'])
@login_required
def query() -> Response:
    user_id = get_jwt_identity()
    input_data = request.get_json()
    return create_query(user_id, input_data)


@query_blueprint.route('/query', methods=['GET'])
@login_required
def get_queries() -> Response:
    user_id = get_jwt_identity()
    return get_user_querries(user_id)


@query_blueprint.route('/query/<int:id>', methods=['GET'])
@login_required
def get_query(id: int) -> Response:
    user_id = get_jwt_identity()
    return get_user_querries(user_id, id)