from abc import ABCMeta
from typing import Optional, Final
from flask import Response
from .format import response
from enum import IntEnum


class HttpStatus(IntEnum):
    OK: Final = 200
    CREATED: Final = 201
    ACCEPTED: Final = 202
    BAD_REQUEST: Final = 400
    UNAUTHORIZED: Final = 401
    FORBIDDEN: Final = 403
    NOT_FOUND: Final = 404

    def is_success(self) -> bool:
        return 200 <= self.value < 300


class HttpError(Exception, metaclass=ABCMeta):
    def __init__(self, data: Optional[object] = None) -> None:
        self.data = data

    def to_response(self) -> Response:
        return response(self.data, getattr(self, '__code__'))


class BadRequest(HttpError):
    __code__: Final[HttpStatus] = HttpStatus.BAD_REQUEST