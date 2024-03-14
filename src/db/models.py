from sqlalchemy import Column, BigInteger, String, Boolean, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from typing import Any, Dict, Optional, final
from datetime import datetime, timezone
from src.db.schemas import Conversation
from pydantic import ValidationError


Base = declarative_base()


@final
class User(Base):
    __tablename__ = 'users'

    tg_user_id = Column(BigInteger, primary_key=True, index=True, autoincrement=False)
    tg_username = Column(String, unique=True, index=True, nullable=False)
    tg_chat_id = Column(BigInteger, unique=True, index=True, autoincrement=False)
    is_active = Column(Boolean, default=True, nullable=False)
    joined_ts = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    posts = relationship('Post', back_populates='user')
           

@final
class Post(Base):
    __tablename__ = 'posts'

    post_id = Column(BigInteger, primary_key=True, index=True)
    conversation = Column(JSON, default=None, nullable=True)
    tg_user_id = Column(BigInteger, ForeignKey('users.tg_user_id'), nullable=False) 
    timestamp = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
        
    user = relationship('User')