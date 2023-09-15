from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from . import Content
from ..user import User
from ..model import Model
from ..query import Query


class ContentResponseBaseSchema(SQLAlchemySchema):
    class Meta:
        model = Content
    generated_at = auto_field(required=True)
    link_to_disk = auto_field(required=True)


class ContentResponseSchema(ContentResponseBaseSchema):
    id = auto_field(required=True)
    query_id = auto_field(required=True)


class ContentInputArgsSchema(SQLAlchemySchema):
    username = auto_field(model=User, required=False)
    model_id = auto_field(column_name='model_id', model=Query, required=False)
    query_id = auto_field(column_name='id', model=Query, required=False)
    type = auto_field(column_name='content_type', model=Model, required=False)
    processing_stage = auto_field(model=Query, required=False)
    generated_before = fields.Date(data_key='generated-before')
    generated_after = fields.Date(data_key='generated-after')