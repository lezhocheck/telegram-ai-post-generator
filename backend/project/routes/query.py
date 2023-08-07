from flask import request, Response, Blueprint
from project.services import create_query
from project.utils.common import login_required
from flask_jwt_extended import get_jwt_identity


query_blueprint = Blueprint('query', __name__)


@query_blueprint.route('/query', methods=['POST'])
@login_required
def query() -> Response:
    user_id = get_jwt_identity()
    input_data = request.get_json()
    return create_query(user_id, input_data)
