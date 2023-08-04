import os
import jwt
from datetime import datetime, timedelta
from .codes import is_success, HTTP_400_BAD_REQUEST
import json
from flask import Response


def format_response(data: object = None, message: str = None, 
                    status: int = HTTP_400_BAD_REQUEST) -> Response:
    result = dict()
    if data is not None:
        if is_success(status):
            result['data'] = data
        else:
            result['errors'] = data
    if message:
        result['message'] = message
    return Response(response=json.dumps(result), status=status)


class Token:
    SECRET_KEY = os.environ.get('SECRET_KEY')
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