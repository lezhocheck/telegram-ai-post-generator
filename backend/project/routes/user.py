from flask_restful import Resource
from flask import request, Response, Blueprint
from project.services import create_user, login_user, refresh_expiring_jwts
from project.utils.common import format_response
from flask_jwt_extended import unset_jwt_cookies


user_blueprint = Blueprint('user', __name__)

class SignUp(Resource):
    @staticmethod
    def post() -> Response:
        input_data = request.get_json()
        return create_user(input_data)
    

class Login(Resource):
    @staticmethod
    def post() -> Response:
        input_data = request.get_json()
        return login_user(input_data)
    

class Logout(Resource):
    @staticmethod
    def post() -> Response:
        response = format_response(message='Successfully logged out')
        unset_jwt_cookies(response)
        return response
    

@user_blueprint.after_request
def refresh(response: Response) -> Response:
    return refresh_expiring_jwts(response)