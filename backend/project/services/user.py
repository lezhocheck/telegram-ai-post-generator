from project.models import SignupUserSchema, User, LoginUserSchema
from project.utils.common import format_response
from flask_jwt_extended import (
    create_access_token, 
    set_access_cookies, 
    get_jwt,
    get_jwt_identity
)
from project.utils.codes import *
from project.extensions import db
from flask import Response
from datetime import datetime, timedelta


def create_user(data: dict) -> Response:
    validation_schema = SignupUserSchema()
    errors = validation_schema.validate(data)
    if errors:
        return format_response(data=errors, status=HTTP_400_BAD_REQUEST)
    
    user_exist = User.query.filter_by(username=data.get('email')).first()
    if user_exist:
        return format_response(message='User already exist', status=HTTP_400_BAD_REQUEST)

    new_user = User(**data)
    new_user.hash_password()
    db.session.add(new_user)
    db.session.commit()
    data.pop('password')
    return format_response(data=data, message='User created', status=HTTP_201_CREATED)


def login_user(data: dict) -> Response:
    validation_schema = LoginUserSchema()
    errors = validation_schema.validate(data)
    if errors:
        return format_response(data=errors, status=HTTP_400_BAD_REQUEST)

    user = User.query.filter_by(email=data.get('email')).first()
    if user is None:
        return format_response(message='User not found', status=HTTP_400_BAD_REQUEST)
    
    if not user.check_password(data.get('password')):
        return format_response(message='Invalid credentials', status=HTTP_400_BAD_REQUEST)
    
    access_token = create_access_token(identity=user.id)
    data.pop('password')
    response = format_response(data=data, message='User logged in successfully', status=HTTP_201_CREATED)
    set_access_cookies(response, access_token)
    return response


def refresh_expiring_jwts(response: Response) -> Response:
    try:
        exp_timestamp = get_jwt()['exp']
        now = datetime.utcnow()
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original response
        return response