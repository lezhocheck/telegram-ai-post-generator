from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from . import Model


class ModelResponseSchema(SQLAlchemySchema):
    class Meta:
        model = Model
    id = auto_field(required=True)
    title = auto_field(required=True)
    content_type = auto_field(required=True, by_value=True)
    description = auto_field(required=True)
    added = auto_field(required=True)
    is_available = auto_field(required=True)


class ModelInputArgsSchema(SQLAlchemySchema):
    title = auto_field(model=Model, required=False)
    added_before = fields.Date(data_key='added-before')
    added_after = fields.Date(data_key='added-after')
    is_available = auto_field(model=Model, required=False)