from .codes import is_success, HTTP_200_OK, HTTP_401_UNAUTHORIZED
from flask import Response, jsonify, g
from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from project.models.user import User


def format_response(data: object = None, message: str = None, 
                    status: int = HTTP_200_OK) -> Response:
    result = dict()
    if data is not None:
        if is_success(status):
            result['data'] = data
        else:
            result['err'] = data
    if message:
        result['msg'] = message
    response = jsonify(result)
    response.status = status
    return response


def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request() 
        user_id = get_jwt_identity()
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return format_response(message='Invalid token', status=HTTP_401_UNAUTHORIZED)
        g.current_user = user
        return fn(*args, **kwargs)
    return wrapper




