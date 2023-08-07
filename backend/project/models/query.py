from project.extensions import db
from enum import Enum
from datetime import datetime
from sqlalchemy.orm import Mapped


class ProcessingStages(str, Enum):
    FINISHED = 'Finished'
    WAITING = 'Waiting'
    FAILED = 'Failed'
    PROCESSING = 'Processing'


class Query(db.Model):
    __tablename__ = 'queries'

    id: Mapped[int] = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = db.Column(db.BigInteger, db.ForeignKey('users.id'))
    model_id: Mapped[int] = db.Column(db.Integer, db.ForeignKey('models.id'))
    prompt: Mapped[str] = db.Column(db.Text)
    timestamp: Mapped[datetime] = db.Column(db.DateTime, default=datetime.utcnow)
    processing_stage: Mapped[ProcessingStages] = db.Column(db.Enum(ProcessingStages), nullable=False)
    content: Mapped['Content'] = db.relationship('Content', uselist=False, backref='contents')

    def __init__(self, **kwargs) -> None:
        self.user_id = kwargs.get('user_id')
        self.model_id = kwargs.get('model_id')
        self.prompt = kwargs.get('prompt')
        self.processing_stage = kwargs.get('processing_stage')
    
    def __repr__(self) -> str:
        return f'<Query id={self.id} prompt={self.prompt}>'