import os
from datetime import timedelta
from typing import Final, Optional, Any


class Config:
    SQLALCHEMY_DATABASE_URI: Final[str] = os.getenv('DATABASE_URL', 'sqlite://')
    SQLALCHEMY_TRACK_MODIFICATIONS: Final[bool] = False
    STATIC_FOLDER: Final[str] = f"{os.getenv('APP_FOLDER')}/project/static"
    CONTENT_FOLDER: Final[str] = f"{os.getenv('APP_FOLDER')}/project/static/content"
    JWT_SECRET_KEY: Final[Optional[str]] = os.getenv('APP_SECRET_KEY')
    JWT_COOKIE_SECURE: Final[Optional[str]] = os.getenv('JWT_COOKIE_SECURE')
    JWT_TOKEN_LOCATION: Final[list[str]] = ['headers']
    JWT_ACCESS_TOKEN_EXPIRES: Final[timedelta] = timedelta(minutes=30)
    JWT_REFRESH_TOKEN_EXPIRES: Final[timedelta] = timedelta(days=15)

    DEFAULT_PAGINATION_PARAMETERS: Final[dict[str, int]] = {
        'page': 1, 
        'page_size': 10, 
        'max_page_size': 100
    }

    API_VERSION: Final[str] = '0.1'
    API_TITLE: Final[str] = 'Models API'
    OPENAPI_VERSION: Final[str] = '3.0.2'
    OPENAPI_URL_PREFIX: Final[str] = '/'
    OPENAPI_SWAGGER_UI_PATH: Final[str] = '/swagger-ui'
    OPENAPI_SWAGGER_UI_URL: Final[str] = 'https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/3.24.2/'
    API_SPEC_OPTIONS: Final[dict[str, Any]] = {
        'security': [{'bearerAuth': []}],
        'components': {
            'securitySchemes': {
                'bearerAuth': {
                    'type': 'http',
                    'scheme': 'bearer',
                    'bearerFormat': 'JWT'
                }
            }
        }
    }

