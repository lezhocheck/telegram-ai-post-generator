from .main import *
from flask_restful import Api
from .main import StaticFolder
from .user import SignUp, Login, Logout


def create_routes(api: Api) -> None:
    api.add_resource(StaticFolder, '/static/<path:filename>')
    api.add_resource(SignUp, '/api/auth/register')
    api.add_resource(Login, '/api/auth/login')
    api.add_resource(Logout, '/api/auth/logout')