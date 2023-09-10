from project.extensions import db
from datetime import datetime
from sqlalchemy.orm import Mapped
from enum import StrEnum
from typing import Final
from .base import BaseModel


class Type(StrEnum):
    IMAGE: Final = 'image'
    VIDEO: Final = 'video'


class State(StrEnum):
    FINISHED: Final = 'Finished'
    FAILED: Final = 'Failed'
    PROCESSING: Final = 'Processing'


class Content(BaseModel, db.Model):
    __tablename__ = 'contents'

    id: Mapped[int] = db.Column(db.BigInteger, db.ForeignKey('queries.id'), 
                                primary_key=True)
    generated: Mapped[datetime] = db.Column(db.DateTime)
    type: Mapped[Type] = db.Column(db.Enum(Type), nullable=False)
    link_to_disk: Mapped[str] = db.Column(db.String(255))
    processing_stage: Mapped[State] = db.Column(db.Enum(State), nullable=False)

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)