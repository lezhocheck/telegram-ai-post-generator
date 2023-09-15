from project.extensions import db
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from project.models.user import User
from http import HTTPStatus
from typing import Any
from project.models.user.schema import (
    UserInputSchema,
    UserResponseSchema,
    UserAuthResponseSchema,
    UserRefreshResponseSchema
)
from project.utils import auth_required
from flask_jwt_extended import (
    get_jwt_identity,
    create_access_token
)


blp = Blueprint(
    'Authentication', 
    __name__,
    url_prefix='/auth'
)


@blp.route('/signup', methods=['POST'])
@blp.arguments(UserInputSchema)
@blp.response(HTTPStatus.CREATED, UserResponseSchema)
@blp.doc(security=[])
def signup(args: dict[str, Any]) -> User:
    user = User(**args)
    user.hash_password()
    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        abort(HTTPStatus.BAD_REQUEST, message='User already signed up')
    except SQLAlchemyError as e:
        db.session.rollback()
        abort(HTTPStatus.BAD_REQUEST, errors=[str(x) for x in e.args])
    return user


@blp.route('/login', methods=['POST'])
@blp.arguments(UserInputSchema)
@blp.response(HTTPStatus.OK, UserAuthResponseSchema)
@blp.doc(security=[])
def login(args: dict[str, Any]) -> User:
    user: User = User.query.filter_by(email=args['email']).first()
    if user is None or not user.check_password(args['password']):
        abort(HTTPStatus.BAD_REQUEST, message='Invalid credentials')
    user.set_tokens()
    return user
    

@blp.route('/refresh', methods=['POST'])
@auth_required(refresh=True)
@blp.response(HTTPStatus.OK, UserRefreshResponseSchema)
def refresh() -> dict[str, str]:
    id = get_jwt_identity()
    access = create_access_token(identity=id)
    return {'access': access}