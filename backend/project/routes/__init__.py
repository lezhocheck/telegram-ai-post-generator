from .main import *
from flask_restful import Api
from .main import StaticFolder
from .user import SignUp


def create_routes(api: Api) -> None:
    api.add_resource(StaticFolder, '/static/<path:filename>')
    api.add_resource(SignUp, '/api/auth/register/')