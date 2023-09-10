from project.extensions import db
from datetime import datetime
from sqlalchemy.orm import Mapped
from .base import BaseModel
from .model import Model
from enum import StrEnum
from typing import Final
from .content import Content
from marshmallow import Schema, fields, validate, ValidationError
from flask import current_app


class Style(StrEnum):
    REALISM: Final = 'Realism'
    IMPRESSIONISM: Final = 'Impressionism'
    CUBISM: Final = 'Cubism'
    SURREALISM: Final = 'Surrealism'
    ABSTRACT: Final = 'Abstract'
    POP_ART: Final = 'Pop Art'
    MINIMALISM: Final = 'Minimalism'
    EXPRESSIONISM: Final = 'Expressionism'
    POINTILLISM: Final = 'Pointillism'
    STREET_ART_GRAFFITI: Final = 'Street Art/Graffiti'
    PHOTOREALISM: Final = 'Photorealism'


class CreateValidator(Schema):
    prompt = fields.Str(required=True, validate=validate.Length(min=1, max=10_000))
    style = fields.Enum(Style, by_value=True, required=True)
    model = fields.Str(required=True)

    def validate_model(self, value):
        with current_app.app_context():
            if not Model.query.filter_by(title=value).first():
                raise ValidationError(f"Model '{value}' does not exist.")


class Query(BaseModel, db.Model):
    __tablename__ = 'queries'
    __validator__ = CreateValidator

    id: Mapped[int] = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = db.Column(db.BigInteger, db.ForeignKey('users.id'))
    model_id: Mapped[int] = db.Column(db.Integer, db.ForeignKey('models.id'))
    prompt: Mapped[str] = db.Column(db.Text, nullable=False)
    style: Mapped[Style] = db.Column(db.Enum(Style), nullable=False)
    timestamp: Mapped[datetime] = db.Column(db.DateTime, default=datetime.utcnow)
    content: Mapped[Content] = db.relationship('Content', uselist=False, 
                                                 backref='contents')

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)