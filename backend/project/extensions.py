from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint


db = SQLAlchemy()


swaggerui_blueprint = get_swaggerui_blueprint(
    base_url='/api/docs',
    api_url='/static/swagger.yml',
    config = { 
        'app_name': 'My application'
    }
)