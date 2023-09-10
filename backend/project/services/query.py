from flask import current_app, Flask, url_for
from project.utils.http import BadRequest, HttpStatus
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
        

class ProcessQuerryThread(threading.Thread):
    def __init__(self, app: Flask, query_id: int, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        path = app.config['STATIC_FOLDER']
        id = f'{uuid.uuid4().hex}.png'
        self._db_session = db.session
        self._local_path = os.path.join(path, id)
        self._public_url = url_for('main.get_from_static', name=id, _external=True)
        self._content = Content.query.filter_by(id=query_id).first()
    
    def run(self) -> None:
        try:
            # TODO
            # SD14Api.run(query, path)
            import time
            time.sleep(5)
            self._content.link_to_disk = self._public_url
            self._content.generated = datetime.utcnow()
            self._content.processing_stage = State.FINISHED
            print(f'Successfully generated content at {self._local_path}')
        except Exception:
            print('Failed generating content')
            traceback.print_exc()
            self._content.processing_stage = State.FAILED
            self._db_session.commit()    


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
    thread = ProcessQuerryThread(current_app, query.id)
    thread.start()
    return query.to_dict(), HttpStatus.CREATED 


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