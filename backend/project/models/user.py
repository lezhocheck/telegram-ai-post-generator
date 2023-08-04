from project.extensions import db
from uuid import uuid4
from datetime import datetime
from flask_bcrypt import generate_password_hash, check_password_hash
from marshmallow import Schema, fields, validate


def UUID() -> str:
    return str(uuid4())


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    username = db.Column(db.String(56), nullable=False, default=UUID)
    email = db.Column(db.String(128), unique=True, nullable=False, index=True)
    password = db.Column(db.String(512), nullable=False)
    joined = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    def __init__(self, **kwargs) -> None:
        self.username = kwargs.get('username')
        self.email = kwargs.get('email')
        self.password = kwargs.get('password')
        self.joined = kwargs.get('joined')
        self.is_active = kwargs.get('is_active')
    
    def __repr__(self) -> str:
        return f'<User id={self.id} username={self.username}>'
    
    def hash_password(self) -> None:
        self.password = generate_password_hash(self.password).decode('utf8')
    
    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)
    

class SignupUserSchema(Schema):
    username = fields.Str(validate=validate.Length(min=4, max=40))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6, max=50))