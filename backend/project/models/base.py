from sqlalchemy.ext.declarative import declarative_base
from typing import Any, Type
from marshmallow import Schema
from project.utils import BadRequest
from typing import Optional


class BaseModel(declarative_base()):
    __abstract__ = True

    def __init__(self, **kwargs) -> None:
        for column in self.__table__.columns:
            setattr(self, column.name, kwargs.get(column.name))

    def to_dict(self) -> dict[str, Any]:
        columns = self.__table__.columns
        result = {}
        for column in columns:
            if column.name not in self.__primary_attrs:
                result[column.name] = getattr(self, column.name)
        return result

    @property
    def __primary_attrs(self) -> list[str]:
        return [attr.name for attr in self.__table__.primary_key.columns.values()]
    
    @classmethod
    def validate(cls, data: dict, 
                 schema: Optional[Schema | Type[Schema]] = None) -> None:
        def construct_schema_object(obj: Schema | Type[Schema]) -> Schema:
            if isinstance(obj, Schema):
                return obj
            return obj() 
        if schema is None:
            attr = getattr(cls, '__validator__')
            schema_obj = construct_schema_object(attr)
        else:
            schema_obj = construct_schema_object(schema)
        errors = schema_obj.validate(data)
        if errors:
            raise BadRequest(errors)
       
    def __repr__(self) -> str:
        name = self.__class__.__name__
        mapped = [(k, getattr(self, k)) for k in self.__primary_attrs]
        return f'<{name}({", ".join(map(lambda x: f"{x[0]}={x[1]}", mapped))})>'
    