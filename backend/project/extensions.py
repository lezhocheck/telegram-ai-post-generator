from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint
from flask import Blueprint
from typing import Final


db: Final[SQLAlchemy] = SQLAlchemy()


swaggerui_blueprint: Final[Blueprint] = get_swaggerui_blueprint(
    base_url='/docs',
    api_url='/static/swagger',
    config = { 
        'app_name': 'My application'
    }
)