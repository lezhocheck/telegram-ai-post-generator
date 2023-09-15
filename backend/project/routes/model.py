from flask_smorest import Blueprint
from http import HTTPStatus
from flask.views import MethodView
from project.models.model.schema import (
    ModelResponseSchema, 
    ModelInputArgsSchema
)
from flask_smorest.pagination import PaginationParameters
from project.utils import auth_required
from project.models.model import Model
from typing import Any


blp = Blueprint(
    'Model', 
    __name__,
    url_prefix='/model'
)


@blp.route('')
class ModelView(MethodView):
    @auth_required(refresh=False)
    @blp.arguments(ModelInputArgsSchema, location='query')
    @blp.response(HTTPStatus.OK, ModelResponseSchema(many=True))
    @blp.paginate()
    def get(self, args: dict[str, Any],
            pagination_parameters: PaginationParameters) -> list[Model]:
        return Model.query.filter_by(**args).paginate(
            page=pagination_parameters.page, 
            per_page=pagination_parameters.page_size
        )


@blp.route('/<int:id>')
class ModelByIdView(MethodView):  
    @auth_required(refresh=False)
    @blp.response(HTTPStatus.OK, ModelResponseSchema)
    def get(self, id: int) -> Model:
        return Model.query.filter_by(id=id).first()