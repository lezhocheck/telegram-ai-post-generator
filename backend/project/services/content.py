from project.extensions import db
from project.models.content import Content
from project.models.query import Query
from project.models.user import User
from typing import Any
from project.utils.error import HttpStatus, BadRequest
from project.utils.paginate import paginated


@paginated
def get_content(user: User) -> tuple[list[dict[str, Any]], HttpStatus]:
    result = db.session.query(Content, Query).join(Query.content)
    result = result.filter(Query.user_id==user.id).all()
    result = [content.to_dict() for content, _ in result]
    if not len(result):
        raise BadRequest('No content')
    return result, HttpStatus.OK


def get_content_by_id(user: User, id: int) -> tuple[dict[str, Any], HttpStatus]:
    result = db.session.query(Content, Query).join(Query.content)
    result = result.filter(Query.user_id==user.id, id==id).first()
    if not result:
        raise BadRequest('No content')
    content, _ = result
    return content.to_dict(), HttpStatus.OK