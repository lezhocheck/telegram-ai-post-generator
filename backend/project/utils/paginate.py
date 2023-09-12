from typing import Callable, Any
from functools import wraps
from flask import request, current_app
from .error import HttpStatus, BadRequest
import math


def paginated(func: Callable[..., tuple[list[dict[str, Any]], HttpStatus]]) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        data, code = func(*args, **kwargs)
        current_page = int(request.args.get('page', 1))
        per_page = current_app.config['ON_PAGE_COUNT']
        start_idx = (current_page - 1) * per_page
        end_idx = start_idx + per_page
        total_pages = math.ceil(len(data) / per_page)
        if current_page < 1 or current_page > total_pages:
            raise BadRequest({'Wrong page argument': current_page})
        result = {
            'page': data[start_idx:end_idx],
            'per_page': per_page,
            'total_pages': total_pages,
            'total_count': len(data)
        }
        return result, code
    return wrapper