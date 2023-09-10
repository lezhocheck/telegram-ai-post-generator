from typing import Callable, Any
from functools import wraps
from flask import request
from .http import HttpStatus


def paginated(func: Callable[..., tuple[list[dict[str, Any]], HttpStatus]]) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        data, code = func(*args, **kwargs)
        current_page = int(request.args.get('page', 1))
        start_idx = (current_page - 1) * 10
        end_idx = start_idx + 10
        return data[start_idx:end_idx], code
    return wrapper