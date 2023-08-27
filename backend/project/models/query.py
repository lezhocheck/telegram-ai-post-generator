from project.extensions import db
from enum import Enum
from datetime import datetime
from sqlalchemy.orm import Mapped


class Styles(str, Enum):
    REALISM = 'Realism'
    IMPRESSIONISM = 'Impressionism'
    CUBISM = 'Cubism'
    SURREALISM = 'Surrealism'
    ABSTRACT = 'Abstract'
    POP_ART = 'Pop Art'
    MINIMALISM = 'Minimalism'
    EXPRESSIONISM = 'Expressionism'
    POINTILLISM = 'Pointillism'
    STREET_ART_GRAFFITI = 'Street Art/Graffiti'
    PHOTOREALISM = 'Photorealism'


class Query(db.Model):
    __tablename__ = 'queries'

    id: Mapped[int] = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = db.Column(db.BigInteger, db.ForeignKey('users.id'))
    model_id: Mapped[int] = db.Column(db.Integer, db.ForeignKey('models.id'))
    prompt: Mapped[str] = db.Column(db.Text, nullable=False)
    style: Mapped[Styles] = db.Column(db.Enum(Styles), nullable=False)
    timestamp: Mapped[datetime] = db.Column(db.DateTime, default=datetime.utcnow)
    content: Mapped['Content'] = db.relationship('Content', uselist=False, backref='contents')

    def __init__(self, **kwargs) -> None:
        self.user_id = kwargs.get('user_id')
        self.model_id = kwargs.get('model_id')
        self.prompt = kwargs.get('prompt')
        self.style = kwargs.get('style')
        self.processing_stage = kwargs.get('processing_stage')

    def as_dict(self) -> dict:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    def __repr__(self) -> str:
        return f'<Query id={self.id} prompt={self.prompt}>'