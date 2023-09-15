import os
from flask import send_from_directory, Response
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from http import HTTPStatus
from project.utils import auth_required


blp = Blueprint(
    'Static', 
    __name__,
    url_prefix='/static'
)


# TODO: Think how to access only genereted content
@blp.route('/<string:filename>')
class StaticContent(MethodView):  
    @auth_required(refresh=False)
    @blp.response(HTTPStatus.OK)
    def get(self, filename: str) -> Response:
        from flask import current_app
        content_dir = current_app.config['CONTENT_FOLDER']
        file = self._find_file_by_name(content_dir, filename)
        return send_from_directory(content_dir, file)

    def _find_file_by_name(self, dir: str, name: str) -> str:
        result = None
        for _, _, files in os.walk(dir):
            fs = [os.path.splitext(f)[0] for f in files]
            try:
                idx = fs.index(name)
                result = files[idx]
            except ValueError:
                pass
        if not result:
            abort(HTTPStatus.BAD_REQUEST, message='File was not found')
        return result