from abc import ABCMeta
from typing import Optional, Final
from flask import Response
from .format import response
from .status import HttpStatus


class HttpError(Exception, metaclass=ABCMeta):
    def __init__(self, data: Optional[object] = None) -> None:
        self.data = data

    def to_response(self) -> Response:
        return response(self.data, getattr(self, '__code__'))


class BadRequest(HttpError):
    __code__: Final[HttpStatus] = HttpStatus.BAD_REQUEST