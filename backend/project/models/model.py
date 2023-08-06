from project.extensions import db
from datetime import datetime
from sqlalchemy.orm import Mapped
from .query import Query


class Model(db.Model):
    __tablename__ = 'models'

    id: Mapped[int] = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = db.Column(db.String(255), nullable=False, unique=True, index=True)
    description: Mapped[str] = db.Column(db.Text)
    added: Mapped[datetime] = db.Column(db.DateTime, default=datetime.utcnow)
    is_available: Mapped[bool] = db.Column(db.Boolean, default=True)
    queries: Mapped[list['Query']] = db.relationship('Query', back_populates='model')

    def __init__(self, **kwargs) -> None:
        self.title = kwargs.get('title')
        self.description = kwargs.get('description')
        self.added = kwargs.get('added')
        self.is_available = kwargs.get('is_available')
    
    def __repr__(self) -> str:
        return f'<Model id={self.id} title={self.title}>'