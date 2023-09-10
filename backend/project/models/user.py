from typing import Any
from project.extensions import db
import uuid
from datetime import datetime
from flask_bcrypt import generate_password_hash, check_password_hash
from sqlalchemy.orm import Mapped
from .query import Query
from .base import BaseModel
from marshmallow import Schema, fields, validate


class SignupValidator(Schema):
    username = fields.Str(validate=validate.Length(min=4, max=56))
    email = fields.Email(required=True, validate=validate.Length(min=3, max=128))
    password = fields.Str(required=True, validate=validate.Length(min=6, max=50))


class LoginValidator(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)


class User(BaseModel, db.Model):
    __tablename__ = 'users'
    __validator__ = SignupValidator

    id: Mapped[int] = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    username: Mapped[str] = db.Column(db.String(56), nullable=False, 
                                      default=str(uuid.uuid4()))
    email: Mapped[str] = db.Column(db.String(128), unique=True, 
                                   nullable=False, index=True)
    password: Mapped[str] = db.Column(db.String(512), nullable=False)
    joined: Mapped[datetime] = db.Column(db.DateTime, default=datetime.utcnow)
    is_active: Mapped[bool] = db.Column(db.Boolean, default=True)
    queries: Mapped[list[Query]] = db.relationship('Query', backref='users')

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
    
    def hash_password(self) -> None:
        self.password = generate_password_hash(self.password).decode('utf8')
    
    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)
    
    def to_dict(self) -> dict[str, Any]:
        data = super().to_dict()
        data.pop('password')
        return data
    