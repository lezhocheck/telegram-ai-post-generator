from project.models import User
from marshmallow import Schema, fields, validate
from project.utils import format_response, HTTP_400_BAD_REQUEST, HTTP_201_CREATED
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token
)
from project.extensions import db
from flask import Response


class SignupSchema(Schema):
    username = fields.Str(validate=validate.Length(min=4, max=40))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6, max=50))


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)


def create_user(data: dict) -> Response:
    validation_schema = SignupSchema()
    errors = validation_schema.validate(data)
    if errors:
        return format_response(data=errors, status=HTTP_400_BAD_REQUEST)
    
    user_exist = db.session.query(User.id).filter_by(email=data.get('email')).first()
    if user_exist:
        return format_response(message='User already exist', status=HTTP_400_BAD_REQUEST)

    new_user = User(**data)
    new_user.hash_password()
    db.session.add(new_user)
    db.session.commit()
    data.pop('password')
    return format_response(data=data, message='User created', status=HTTP_201_CREATED)


def login_user(data: dict) -> Response:
    validation_schema = LoginSchema()
    errors = validation_schema.validate(data)
    if errors:
        return format_response(data=errors, status=HTTP_400_BAD_REQUEST)

    user = User.query.filter_by(email=data.get('email')).first()
    if user is None:
        return format_response(message='User not found', status=HTTP_400_BAD_REQUEST)
    
    if not user.check_password(data.get('password')):
        return format_response(message='Invalid credentials', status=HTTP_400_BAD_REQUEST)
    
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    data.pop('password')
    data['tokens'] = {'access': access_token, 'refresh': refresh_token}
    return format_response(data=data, message='User logged in successfully', status=HTTP_201_CREATED)