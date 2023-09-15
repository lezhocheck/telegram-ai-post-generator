from marshmallow import fields
from marshmallow_sqlalchemy import auto_field, SQLAlchemySchema
from . import Query
from ..user import User
from ..content.schema import ContentResponseBaseSchema


class QueryCreateSchema(SQLAlchemySchema):
    class Meta:
        model = Query
    prompt = auto_field(required=True)
    style = auto_field(required=True, by_value=True)
    model_id = auto_field(required=True)


class QueryResponseSchema(SQLAlchemySchema):
    class Meta:
        model = Query
    id = auto_field(model=Query, required=True)
    username = auto_field(model=User, required=True)
    model_id = auto_field(model=Query, required=True)
    prompt = auto_field(model=Query, required=True)
    style = auto_field(model=Query, required=True, by_value=True)
    timestamp = auto_field(model=Query, required=True)
    processing_stage = auto_field(model=Query, required=True, by_value=True)
    content = fields.Nested(ContentResponseBaseSchema, many=True)
