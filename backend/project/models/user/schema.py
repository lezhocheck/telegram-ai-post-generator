from marshmallow import Schema, fields, validate
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from . import User


class UserInputSchema(SQLAlchemySchema):
    class Meta:
        model = User
    email = auto_field(required=True)
    password = auto_field(required=True)
    username = auto_field(required=False)


class UserResponseSchema(SQLAlchemySchema):
    class Meta:
        model = User
    id = auto_field(required=True)
    email = auto_field(required=True)
    username = auto_field(required=True)
    joined = auto_field(required=True)
    is_active = auto_field(required=True)


class UserAuthResponseSchema(UserResponseSchema):
    tokens = fields.Dict(
        required=True,
        keys=fields.Str(required=True, validate=validate.Equal(['access', 'refresh'])), 
        values=fields.Str(required=True),
        validate=validate.Length(equal=2)
    )


class UserRefreshResponseSchema(Schema):
    access = fields.Str(required=True)