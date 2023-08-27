from project.extensions import db
from project.models import Content, Query
from flask import Response
from project.utils import format_response, HTTP_200_OK, HTTP_400_BAD_REQUEST


def get_user_content(user_id: int, id: [int, None] = None) -> Response:
    if id is None:
        result = db.session.query(Content, Query).join(Query.content).filter(Query.user_id==user_id).all()
        result = [content.as_dict() for content, query in result]
    else:
        result = db.session.query(Content).filter_by(id=id).first()
        if not result:
            return format_response(message='No content', status=HTTP_400_BAD_REQUEST)
        result = result.as_dict()
    return format_response(data=result, status=HTTP_200_OK)