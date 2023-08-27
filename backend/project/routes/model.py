from flask import Response, Blueprint
from project.services.model import get_models
from project.utils.common import login_required


model_blueprint = Blueprint('model', __name__)


@model_blueprint.route('/model', methods=['GET'])
@login_required
def get_queries() -> Response:
    return get_models()


@model_blueprint.route('/model/<int:id>', methods=['GET'])
@login_required
def get_query(id: int) -> Response:
    return get_models(id)