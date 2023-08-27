from flask import Response, current_app, Flask
from project.utils import format_response, HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_200_OK
from project.models import Model, Query, Styles, ProcessingStages, Content, ContentType
from project.extensions import db
from marshmallow import Schema, fields, validate, ValidationError
import os
from project.nn.sd14 import SD14Api
import traceback
import threading
from datetime import datetime
import uuid


class CreateQuerySchema(Schema):
    prompt = fields.Str(required=True, validate=validate.Length(min=1, max=100_000))
    style = fields.Enum(Styles, by_value=True, required=True)
    model = fields.Str(required=True)

    def validate_model(self, value):
        with current_app.app_context():
            if not db.session.query(Model).filter_by(title=value).first():
                raise ValidationError(f"Model '{value}' does not exist.")
        

def create_query(id: int, data: dict) -> Response:
    validation_schema = CreateQuerySchema()
    errors = validation_schema.validate(data)
    if errors:
        return format_response(data=errors, status=HTTP_400_BAD_REQUEST)
    
    model = db.session.query(Model).filter_by(title=data.pop('model')).first()
    if not model:
        return format_response(message='Invalid model', status=HTTP_400_BAD_REQUEST)

    data['user_id'] = id
    data['model_id'] = model.id
    data['processing_stage'] = ProcessingStages.WAITING
    new_query = Query(**data)
    db.session.add(new_query)
    db.session.flush()
    db.session.commit()

    after_query_insert(new_query)
    return format_response(data=data, message='Query added', status=HTTP_201_CREATED)


def get_path() -> os.path:
    path = current_app.config['MEDIA_FOLDER']
    id = uuid.uuid4().hex
    return os.path.join(path, f'{id}.png')


def after_query_insert(target: Query):
    query = f'{target.prompt}'
    content = Content(type=ContentType.IMAGE, 
                      processing_stage=ProcessingStages.PROCESSING,
                      query_id=target.id)
    db.session.add(content)
    db.session.flush()
    db.session.commit()

    path = get_path()

    def process(app: Flask):
        with app.app_context():
            selected = Content.query.get(content.id)
            try:
                SD14Api.run(query, path)
                selected.link_to_disk = path
                selected.generated = datetime.utcnow()
                selected.processing_stage = ProcessingStages.FINISHED
                print(f'Successfully generated content at {path}')
            except Exception:
                print('Failed generating content')
                traceback.print_exc()
                selected.processing_stage = ProcessingStages.FAILED
            print(selected.as_dict())
            db.session.commit()
            
    thread = threading.Thread(target=process, kwargs={'app': current_app._get_current_object()})
    thread.start()

def get_user_querries(user_id: int, id: [int, None] = None) -> Response:
    if id is None:
        result = db.session.query(Query).filter_by(user_id=user_id).all()
        result = [i.as_dict() for i in result if i]
    else:
        result = db.session.query(Query).filter_by(user_id=user_id, id=id).first()
        if not result:
            return format_response(message='No queries', status=HTTP_400_BAD_REQUEST)
        result = result.as_dict()
    return format_response(data=result, status=HTTP_200_OK)
