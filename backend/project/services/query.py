from flask import Response, current_app
from project.utils import format_response, HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_200_OK
from project.models import Model, Query, ProcessingStages
from project.extensions import db
from marshmallow import Schema, fields, validate, ValidationError


class CreateQuerySchema(Schema):
    prompt = fields.Str(required=True, validate=validate.Length(min=1, max=100_000))
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
    db.session.commit()

    return format_response(data=data, message='Query added', status=HTTP_201_CREATED)


def get_user_querries(user_id: int, id: [int, None] = None) -> Response:
    if id is None:
        result = db.session.query(Query).filter_by(user_id=user_id).all()
        result = [i.as_dict() for i in result]
    else:
        result = db.session.query(Query).filter_by(user_id=user_id, id=id).first()
        result = result.as_dict()
    return format_response(data=result, status=HTTP_200_OK)