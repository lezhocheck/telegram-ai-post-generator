from flask import request, Response, Blueprint
from project.services.user import login_required
from project.utils.format import response
from project.models.user import User
from project.services.query import create_query, get_queries, get_query_by_id


query_blueprint = Blueprint('query', __name__)


@query_blueprint.route('/query', methods=['POST'])
@login_required
def add_query(user: User) -> Response:
    input_data = request.get_json()
    data, code = create_query(user, input_data)
    return response(data, code)


@query_blueprint.route('/query', methods=['GET'])
@login_required
def select_queries(user: User) -> Response:
    data, code = get_queries(user)
    return response(data, code)

@query_blueprint.route('/query/<int:id>', methods=['GET'])
@login_required
def select_query(user: User, id: int) -> Response:
    data, code = get_query_by_id(user, id)
    return response(data, code)