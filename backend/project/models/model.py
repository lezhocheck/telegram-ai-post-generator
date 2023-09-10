from project.extensions import db
from datetime import datetime
from sqlalchemy.orm import Mapped
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .query import Query
from .base import BaseModel


class Model(BaseModel, db.Model):
    __tablename__ = 'models'

    id: Mapped[int] = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = db.Column(db.String(255), nullable=False, 
                                   unique=True, index=True)
    description: Mapped[str] = db.Column(db.Text)
    added: Mapped[datetime] = db.Column(db.DateTime, default=datetime.utcnow)
    is_available: Mapped[bool] = db.Column(db.Boolean, default=True)
    queries: Mapped[list['Query']] = db.relationship('Query', backref='models')

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)