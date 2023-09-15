from project.extensions import db
from datetime import datetime
from sqlalchemy.orm import Mapped


class Content(db.Model):
    __tablename__ = 'contents'

    id: Mapped[int] = db.Column(db.Integer, primary_key=True, autoincrement=True)
    query_id: Mapped[int] = db.Column(db.BigInteger, db.ForeignKey('queries.id'))
    generated_at: Mapped[datetime] = db.Column(db.DateTime)
    link_to_disk: Mapped[str] = db.Column(db.String(255))