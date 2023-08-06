import jwt
from datetime import datetime, timedelta
from .codes import is_success, HTTP_200_OK
from flask import Response, jsonify
import os


def format_response(data: object = None, message: str = None, 
                    status: int = HTTP_200_OK) -> Response:
    result = dict()
    if data is not None:
        if is_success(status):
            result['data'] = data
        else:
            result['errors'] = data
    if message:
        result['message'] = message
    response = jsonify(result)
    response.status = status
    return response


class Token:
    SECRET_KEY = os.getenv('APP_SECRET_KEY')
    ALGORITHM = 'HS256'

    @staticmethod
    def encode(identifier: int) -> str:
        payload = {
            'exp': datetime.utcnow() + timedelta(minutes=15),
            'id': str(identifier)
        }
        token = jwt.encode(payload, Token.SECRET_KEY, algorithm=Token.ALGORITHM)
        return token

    @staticmethod
    def decode(token: str) -> dict:
        return jwt.decode(token, Token.SECRET_KEY,
                          algorithms=Token.ALGORITHM,
                          options={'require_exp': True})