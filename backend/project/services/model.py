from project.extensions import db
from project.models import Model
from flask import Response
from project.utils import format_response, HTTP_200_OK, HTTP_400_BAD_REQUEST


def get_models(id: [int, None] = None) -> Response:
    if id is None:
        result = db.session.query(Model).all()
        result = [model.as_dict() for model in result]
    else:
        result = db.session.query(Model).filter_by(id=id).first()
        if not result:
            return format_response(message='No content', status=HTTP_400_BAD_REQUEST)
        result = result.as_dict()
    return format_response(data=result, status=HTTP_200_OK)