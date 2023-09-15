from project.extensions import db
import uuid
from datetime import datetime
from flask_bcrypt import generate_password_hash, check_password_hash
from sqlalchemy.orm import Mapped
from ..query import Query
from flask_jwt_extended import create_access_token, create_refresh_token


class User(db.Model):
    __tablename__ = 'users'

    id: Mapped[int] = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    username: Mapped[str] = db.Column(db.String(56), nullable=False, 
                                      default=str(uuid.uuid4()))
    email: Mapped[str] = db.Column(db.String(128), unique=True, 
                                   nullable=False, index=True)
    password: Mapped[str] = db.Column(db.String(512), nullable=False)
    joined: Mapped[datetime] = db.Column(db.DateTime, default=datetime.utcnow)
    is_active: Mapped[bool] = db.Column(db.Boolean, default=True)
    queries: Mapped[list[Query]] = db.relationship('Query', backref='users')
    
    def hash_password(self) -> None:
        self.password = generate_password_hash(self.password).decode('utf8')
    
    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)
    
    def set_tokens(self) -> None:
        if not isinstance(self.id, int):
            raise ValueError('User must have valid id')
        self.tokens = {
            'access': create_access_token(identity=self.id), 
            'refresh': create_refresh_token(identity=self.id)
        }
    