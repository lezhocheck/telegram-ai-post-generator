from flask import Response, Blueprint
from project.services.model import get_all_models, get_model_by_id
from project.services.user import login_required
from project.models.user import User
from project.utils.format import response


model_blueprint = Blueprint('model', __name__)


@model_blueprint.route('/model', methods=['GET'])
@login_required
def select_models(_: User) -> Response:
    data, code = get_all_models()
    return response(data, code)


@model_blueprint.route('/model/<int:id>', methods=['GET'])
@login_required
def select_model(_: User, id: int) -> Response:
    data, code = get_model_by_id(id)
    return response(data, code)