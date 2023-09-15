from project.extensions import db
from datetime import datetime
from sqlalchemy.orm import Mapped
from ..query import Query
from enum import StrEnum
from typing import Final


class Type(StrEnum):
    IMAGE_PNG: Final = 'png'
    VIDEO_MP4: Final = 'mp4'
    GIF: Final = 'gif'


class Model(db.Model):
    __tablename__ = 'models'

    id: Mapped[int] = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = db.Column(db.String(255), nullable=False, 
                                   unique=True, index=True)
    content_type: Mapped[Type] = db.Column(db.Enum(Type), nullable=False)
    description: Mapped[str] = db.Column(db.String(30_000))
    added: Mapped[datetime] = db.Column(db.DateTime, default=datetime.utcnow)
    is_available: Mapped[bool] = db.Column(db.Boolean, default=True)
    queries: Mapped[list[Query]] = db.relationship('Query', backref='models')