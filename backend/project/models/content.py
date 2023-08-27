from project.extensions import db
from datetime import datetime
from sqlalchemy.orm import Mapped
from enum import Enum


class ContentType(str, Enum):
    IMAGE = 'image'
    VIDEO = 'video'


class ProcessingStages(str, Enum):
    FINISHED = 'Finished'
    WAITING = 'Waiting'
    FAILED = 'Failed'
    PROCESSING = 'Processing'


class Content(db.Model):
    __tablename__ = 'contents'

    id: Mapped[int] = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    generated: Mapped[datetime] = db.Column(db.DateTime)
    type: Mapped[ContentType] = db.Column(db.Enum(ContentType), nullable=False)
    link_to_disk: Mapped[str] = db.Column(db.String(255))
    query_id: Mapped[int] = db.Column(db.BigInteger, db.ForeignKey('queries.id'))
    processing_stage: Mapped[ProcessingStages] = db.Column(db.Enum(ProcessingStages), nullable=False)

    def __init__(self, **kwargs) -> None:
        self.generated = kwargs.get('generated')
        self.type = kwargs.get('type')
        self.link_to_disk = kwargs.get('link_to_disk')
        self.processing_stage = kwargs.get('processing_stage')
        self.query_id = kwargs['query_id']
    
    def as_dict(self) -> dict:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    def __repr__(self) -> str:
        return f'<Content id={self.id} type={self.type}>'