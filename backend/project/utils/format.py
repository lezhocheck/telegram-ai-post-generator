from typing import Optional
from flask import jsonify, Response
from .http import HttpStatus


def response(data: Optional[object], status: HttpStatus) -> Response:
    result = dict()
    if data is not None:
        if isinstance(data, str):
            result['message'] = data
        elif status.is_success():
            result['data'] = data
        else:
            result['errors'] = data
    response = jsonify(result)
    response.status = status.value
    return response