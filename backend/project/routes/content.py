from flask_smorest import Blueprint
from flask_smorest.pagination import PaginationParameters
from flask.views import MethodView
from http import HTTPStatus
from project.models.content import Content
from project.models.content.schema import (
    ContentResponseSchema,
    ContentInputArgsSchema
)
from project.utils import auth_required
from typing import Any


blp = Blueprint(
    'Content', 
    __name__,
    url_prefix='/content'
)


@blp.route('')
class ContentView(MethodView):
    @auth_required(refresh=False)
    @blp.arguments(ContentInputArgsSchema, location='query')
    @blp.response(HTTPStatus.OK, ContentResponseSchema(many=True))
    @blp.paginate()
    def get(self, args: dict[str, Any],
            pagination_parameters: PaginationParameters) -> list[Content]:
        return Content.query.paginate(
            page=pagination_parameters.page, 
            per_page=pagination_parameters.page_size
        )


@blp.route('/<int:id>')
class ContentByIdView(MethodView):  
    @auth_required(refresh=False)
    @blp.response(HTTPStatus.OK, ContentResponseSchema)
    def get(self, id: int) -> Content:
        return Content.query.filter_by(id=id).first()