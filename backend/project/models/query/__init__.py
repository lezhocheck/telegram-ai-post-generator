from project.extensions import db
from datetime import datetime
from sqlalchemy.orm import Mapped
from enum import StrEnum
from typing import Final
from ..content import Content


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


class Stage(StrEnum):
    FINISHED: Final = 'Finished'
    FAILED: Final = 'Failed'
    PROCESSING: Final = 'Processing'


class Query(db.Model):
    __tablename__ = 'queries'

    id: Mapped[int] = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = db.Column(db.BigInteger, db.ForeignKey('users.id'))
    model_id: Mapped[int] = db.Column(db.Integer, db.ForeignKey('models.id'))
    prompt: Mapped[str] = db.Column(db.String(10_000), nullable=False)
    style: Mapped[Style] = db.Column(db.Enum(Style), nullable=False)
    timestamp: Mapped[datetime] = db.Column(db.DateTime, default=datetime.utcnow)
    processing_stage: Mapped[Stage] = db.Column(db.Enum(Stage), nullable=False, 
                                                default=Stage.PROCESSING)
    content: Mapped[Content] = db.relationship('Content', backref='contents')