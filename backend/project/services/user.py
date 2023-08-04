from project.models import SignupUserSchema, User
from project.utils.common import format_response
from project.utils.codes import *
from project.extensions import db
from flask import Response


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