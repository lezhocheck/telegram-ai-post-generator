from project.extensions import db
from enum import Enum
from datetime import datetime
from sqlalchemy.orm import Mapped


class ProcessingStages(Enum):
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
    content: Mapped['Content'] = db.relationship('Content', back_populates='query')

    def __init__(self, **kwargs) -> None:
        self.prompt = kwargs.get('prompt')
    
    def __repr__(self) -> str:
        return f'<Query id={self.id} prompt={self.prompt}>'