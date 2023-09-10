from flask import request, Response, Blueprint
from project.services.user import create_user, login_user
from project.utils.http import response, HttpStatus
from flask_jwt_extended import (
    unset_jwt_cookies, 
    jwt_required, 
    get_jwt_identity,
    create_access_token
)


user_blueprint = Blueprint('user', __name__)


@user_blueprint.route('/auth/signup', methods=['POST'])
def signup() -> Response:
    input_data = request.get_json()
    data, code = create_user(input_data)
    return response(data, code)


@user_blueprint.route('/auth/login', methods=['POST'])
def login() -> Response:
    input_data = request.get_json()
    data, code = login_user(input_data)
    return response(data, code)


@user_blueprint.route('/auth/logout', methods=['POST'])
def logout() -> Response:
    result = response('Successfully logged out', HttpStatus.OK)
    unset_jwt_cookies(result)
    return result
    

@user_blueprint.route('/auth/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh() -> Response:
    id = get_jwt_identity()
    access_token = create_access_token(identity=id)
    result = {'tokens': {'access': access_token}}
    return response(result, HttpStatus.OK)