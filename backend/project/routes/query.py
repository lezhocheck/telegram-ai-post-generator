from project.extensions import db
from flask_smorest import Blueprint, abort
from http import HTTPStatus
from flask.views import MethodView
from flask import current_app, Flask
from project.models.query.schema import (
    QueryResponseSchema, 
    QueryCreateSchema
)
from flask_smorest.pagination import PaginationParameters
from project.utils import auth_required
from flask_jwt_extended import get_jwt_identity
from project.models.query import Query, Stage
from project.models.user import User
from project.models.model import Model
from typing import Any
import threading
from project.api.sd14 import BaseApi


blp = Blueprint(
    'Query', 
    __name__,
    url_prefix='/query'
)


class ProcessQueryThread(threading.Thread):
    def __init__(self, query: Query, model: Model, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._query = query
        self._model = model
        self._app: Flask = getattr(current_app, '_get_current_object')()
    
    def run(self) -> None:
        with self._app.app_context(), self._app.test_request_context():
            try:
                api = BaseApi.from_model(self._model)
                content = next(api.run(self._query))
                db.session.add(content)
                self._query.processing_stage = Stage.FAILED
                db.session.commit()
                print(f'Successfully generated {content}')
            except Exception:
                db.session.rollback()
                import traceback
                print('Failed generating content')
                traceback.print_exc()
                self._query.processing_stage = Stage.FAILED
                db.session.commit()    


@blp.route('')
class QueryView(MethodView):
    @auth_required(refresh=False)
    @blp.arguments(QueryCreateSchema)
    @blp.response(HTTPStatus.OK, QueryResponseSchema)
    def post(self, args: dict[str, Any]) -> Query:
        user_id: int = get_jwt_identity()
        model = Model.query.filter_by(id=args['model_id']).first()
        if not model:
            abort(HTTPStatus.BAD_REQUEST, 'Invalid model id')
        query = Query(**args, user_id=user_id)
        db.session.add(query)
        db.session.commit()
        thread = ProcessQueryThread(query, model)
        thread.run()
        return query

    @auth_required(refresh=False)
    @blp.response(HTTPStatus.OK, QueryResponseSchema(many=True))
    @blp.paginate()
    def get(self, pagination_parameters: PaginationParameters) -> list[Query]:
        user_id: int = get_jwt_identity()
        return Query.query.paginate(
            page=pagination_parameters.page, 
            per_page=pagination_parameters.page_size
        )


@blp.route('/<int:id>')
class QueryByIdView(MethodView):  
    @auth_required(refresh=False)
    @blp.response(HTTPStatus.OK, QueryResponseSchema)
    def get(self, id: int) -> Query:
        user_id: int = get_jwt_identity()
        return Query.query                          \
            .join(User, Query.user_id == User.id)   \
            .filter(Query.id == id, 
                    User.id == user_id)             \
            .first()