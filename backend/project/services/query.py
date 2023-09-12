from flask import current_app, url_for, Flask
from project.utils.error import BadRequest, HttpStatus
from project.models.query import Query
from project.models.content import Content, Type, State
from project.models.model import Model
from project.models.user import User
from project.extensions import db
import os
from project.api.sd14 import SD14Api
import traceback
import threading
from typing import Any
from datetime import datetime
import uuid
from project.utils.paginate import paginated
        

class ProcessQueryThread(threading.Thread):
    def __init__(self, query_id: int, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._query_id = query_id
        path = current_app.config['STATIC_FOLDER']
        id = f'{uuid.uuid4().hex}.png'
        self._local_path = os.path.join(path, id)
        self._public_url = url_for('main.get_from_static', name=id, _external=True)
        self._app: Flask = getattr(current_app, '_get_current_object')()
    
    def run(self) -> None:
        with self._app.app_context():
            query = Query.query.filter_by(id=self._query_id).first()
            content = Content.query.filter_by(id=self._query_id).first()
            try:
                SD14Api.run(query.prompt, self._local_path)
                content.link_to_disk = self._public_url
                content.generated = datetime.utcnow()
                content.processing_stage = State.FINISHED
                print(f'Successfully generated content at {self._local_path}')
            except Exception:
                print('Failed generating content')
                traceback.print_exc()
                content.processing_stage = State.FAILED
            db.session.commit()    


def create_query(user: User, data: dict[str, Any]) -> tuple[dict[str, Any], HttpStatus]:
    Query.validate(data)
    model = Model.query.filter_by(title=data.pop('model')).first()
    query = Query(**data, user_id=user.id, model_id=model.id)
    db.session.add(query)
    db.session.flush()
    content = Content(id=query.id,
                      type=Type.IMAGE, 
                      processing_stage=State.PROCESSING)
    db.session.add(content)
    db.session.commit()
    thread = ProcessQueryThread(query.id)
    thread.start()
    return query.to_dict(), HttpStatus.CREATED 


@paginated
def get_queries(user: User) -> tuple[list[dict[str, Any]], HttpStatus]:
    result = Query.query.filter_by(user_id=user.id).all()
    result = [query.to_dict() for query in result]
    if not len(result):
        raise BadRequest('No queries')
    return result, HttpStatus.OK


def get_query_by_id(user: User, id: int) -> tuple[dict[str, Any], HttpStatus]:
    result = Query.query.filter_by(id=id, user_id=user.id).all()
    if not result:
        raise BadRequest('No content')
    return result.to_dict(), HttpStatus.OK