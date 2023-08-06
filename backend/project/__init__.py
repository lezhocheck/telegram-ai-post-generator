from flask import Flask
from project.extensions import db, swaggerui_blueprint
from project.routes import main_blueprint
from project.routes.user import user_blueprint
from flask_restful import Api
from flask_jwt_extended import JWTManager
from project.routes import create_routes


def register_blueprints(app: Flask) -> None:
    app.register_blueprint(swaggerui_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(user_blueprint)


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object('project.config.Config')

    jwt = JWTManager(app)

    api = Api(app)
    create_routes(api)
    db.init_app(app)
    register_blueprints(app)
    return app


app = create_app()