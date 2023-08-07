from flask import request, Response, Blueprint
from project.services import create_user, login_user
from project.utils.common import format_response
from flask_jwt_extended import unset_jwt_cookies, jwt_required, get_jwt_identity, create_access_token


user_blueprint = Blueprint('user', __name__)


@user_blueprint.route('/auth/signup', methods=['POST'])
def signup() -> Response:
    input_data = request.get_json()
    return create_user(input_data)


@user_blueprint.route('/auth/login', methods=['POST'])
def login() -> Response:
    input_data = request.get_json()
    return login_user(input_data)  


@user_blueprint.route('/auth/logout', methods=['POST'])
def logout() -> Response:
    response = format_response(message='Successfully logged out')
    unset_jwt_cookies(response)
    return response 
    

@user_blueprint.route('/auth/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh() -> Response:
    id = get_jwt_identity()
    access_token = create_access_token(identity=id)
    return format_response(data={'tokens': {'access': access_token}})