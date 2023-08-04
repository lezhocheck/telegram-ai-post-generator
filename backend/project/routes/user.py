from flask_restful import Resource
from flask import request, Response
from project.services import create_user


class SignUp(Resource):
    @staticmethod
    def post() -> Response:
        input_data = request.get_json()
        return create_user(input_data)