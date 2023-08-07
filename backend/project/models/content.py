from project.extensions import db
from datetime import datetime
from sqlalchemy.orm import Mapped
from enum import Enum


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


class Content(db.Model):
    __tablename__ = 'contents'

    id: Mapped[int] = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    generated: Mapped[datetime] = db.Column(db.DateTime, default=datetime.utcnow)
    type: Mapped[str] = db.Column(db.String(255), nullable=False)
    style: Mapped[Styles] = db.Column(db.Enum(Styles), nullable=False)
    link_to_disk: Mapped[str] = db.Column(db.String(255), nullable=False)
    keywords: Mapped[str] = db.Column(db.Text)
    query_id: Mapped[int] = db.Column(db.BigInteger, db.ForeignKey('queries.id'))

    def __init__(self, **kwargs) -> None:
        self.type = kwargs.get('type')
        self.style = kwargs.get('style')
        self.link_to_disk = kwargs.get('link_to_disk')
        self.keywords = kwargs.get('keywords')
    
    def as_dict(self) -> dict:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    def __repr__(self) -> str:
        return f'<Content id={self.id} type={self.type}>'