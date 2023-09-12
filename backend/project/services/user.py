from project.models.user import User, LoginValidator
from project.utils.error import BadRequest, HttpStatus
from functools import wraps
from typing import Any, Callable
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token
)
from project.extensions import db
from flask import g


def login_required(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request() 
        user_id = get_jwt_identity()
        user = User.query.filter_by(id=user_id).first()
        if not user:
            raise BadRequest('Invalid token')
        g.current_user = user
        return func(user, *args, **kwargs)
    return wrapper


def create_user(data: dict[str, Any]) -> tuple[dict[str, Any], HttpStatus]:
    User.validate(data)
    if User.query.filter_by(email=data['email']).first():
        raise BadRequest('User already exists')
    user = User(**data)
    user.hash_password()
    db.session.add(user)
    db.session.commit()
    return user.to_dict(), HttpStatus.CREATED


def login_user(data: dict[str, Any]) -> tuple[dict[str, Any], HttpStatus]:
    User.validate(data, LoginValidator)
    user: User | None = User.query.filter_by(email=data.get('email')).first()
    if user is None or not user.check_password(data['password']):
        raise BadRequest('Invalid credentials')
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    data = user.to_dict()
    data['tokens'] = {'access': access_token, 'refresh': refresh_token}
    return data, HttpStatus.OK