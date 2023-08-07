from flask import request, Response, Blueprint
from project.services import create_user, login_user, refresh_tokens
from project.utils.common import format_response
from flask_jwt_extended import unset_jwt_cookies


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
    

@user_blueprint.after_request
def refresh(response: Response) -> Response:
    return refresh_tokens(response)