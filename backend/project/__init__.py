from flask import Flask
from project.extensions import db
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS


def register_blueprints(api: Api) -> None:
    from project.routes.user import blp as user_blueprint
    from project.routes.query import blp as query_blueprint
    from project.routes.main import blp as main_blueprint
    from project.routes.content import blp as content_blueprint
    from project.routes.model import blp as model_blueprint

    api.register_blueprint(main_blueprint)
    api.register_blueprint(user_blueprint)
    api.register_blueprint(query_blueprint)
    api.register_blueprint(content_blueprint)
    api.register_blueprint(model_blueprint)


def register_jwt(app: Flask) -> None:
    from http import HTTPStatus
    from flask import make_response, Response, jsonify

    jwt = JWTManager(app)

    def handle(status: HTTPStatus, message: str) -> Response:
        payload = {
            'code': status.value,
            'message': message,
            'status': status.phrase
        }
        return make_response(jsonify(payload), status)
    
    jwt.invalid_token_loader(
        lambda *_: handle(
            HTTPStatus.UNPROCESSABLE_ENTITY, 
            message='Invalid token'
        )
    )
    jwt.expired_token_loader(
        lambda *_: 
        handle(
            HTTPStatus.BAD_REQUEST, 
            message='Token expired'
        )
    )
    jwt.unauthorized_loader(
        lambda *_: handle(
            HTTPStatus.UNAUTHORIZED, 
            message='Unauthorized'
        )
    )
    jwt.token_verification_failed_loader(
        lambda *_: handle(
            HTTPStatus.UNPROCESSABLE_ENTITY, 
            message='Token verification failed'
        )
    )


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object('project.config.Config')
    api = Api(app)
    CORS(app)
    register_jwt(app)
    db.init_app(app)
    register_blueprints(api)
    return app