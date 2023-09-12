import os
from datetime import timedelta
from typing import Final, Optional


class Config:
    SQLALCHEMY_DATABASE_URI: Final[str] = os.getenv('DATABASE_URL', 'sqlite://')
    SQLALCHEMY_TRACK_MODIFICATIONS: Final[bool] = False
    STATIC_FOLDER: Final[Optional[str]] = f"{os.getenv('APP_FOLDER')}/project/static"
    JWT_SECRET_KEY: Final[Optional[str]] = os.getenv('APP_SECRET_KEY')
    JWT_COOKIE_SECURE: Final[Optional[str]] = os.getenv('JWT_COOKIE_SECURE')
    JWT_TOKEN_LOCATION: Final[list[str]] = ['headers']
    JWT_ACCESS_TOKEN_EXPIRES: Final[timedelta] = timedelta(minutes=30)
    JWT_REFRESH_TOKEN_EXPIRES: Final[timedelta] = timedelta(days=15)
    ON_PAGE_COUNT: Final = 10
