from enum import IntEnum
from typing import Final


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