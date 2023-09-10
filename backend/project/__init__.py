from flask import Flask
from project.extensions import db, swaggerui_blueprint
from project.routes.user import user_blueprint
from project.routes.query import query_blueprint
from project.routes.main import main_blueprint
from project.routes.content import content_blueprint
from project.routes.model import model_blueprint
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from project.utils.http import BadRequest


def register_blueprints(app: Flask) -> None:
    app.register_blueprint(swaggerui_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(query_blueprint)
    app.register_blueprint(content_blueprint)
    app.register_blueprint(model_blueprint)


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object('project.config.Config')
    JWTManager(app)
    CORS(app)
    Api(app)
    db.init_app(app)
    register_blueprints(app)
    app.register_error_handler(BadRequest, lambda e: e.to_response())
    return app