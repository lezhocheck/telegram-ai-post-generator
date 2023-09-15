from project.models.user import User
from flask import g
from typing import Callable
from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from flask_smorest import abort
from http import HTTPStatus


def auth_required(refresh: bool = False) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request(refresh=refresh) 
            user = User.query.filter_by(id=get_jwt_identity()).first()
            if not user:
                abort(HTTPStatus.UNAUTHORIZED, message='Invalid access token')
            g.current_user = user
            return func(*args, **kwargs)
        return wrapper
    return decorator