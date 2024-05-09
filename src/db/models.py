from sqlalchemy import Column, BigInteger, String, Boolean, DateTime, JSON, ForeignKey, Integer
from sqlalchemy.orm import relationship, declarative_base
from typing import final
from datetime import datetime, timezone


Base = declarative_base()


@final
class User(Base):
    __tablename__ = 'users'

    tg_user_id = Column(BigInteger().with_variant(Integer, 'sqlite'), primary_key=True, index=True, autoincrement=False)
    tg_username = Column(String, unique=True, index=True, nullable=False)
    tg_chat_id = Column(BigInteger().with_variant(Integer, 'sqlite'), unique=True, index=True, autoincrement=False)
    is_active = Column(Boolean, default=True, nullable=False)
    joined_ts = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    posts = relationship('Post', back_populates='user')
           

@final
class Post(Base):
    __tablename__ = 'posts'

    post_id = Column(BigInteger().with_variant(Integer, 'sqlite'), primary_key=True, index=True, autoincrement=True)
    conversation = Column(JSON, default=None, nullable=True)
    tg_user_id = Column(BigInteger().with_variant(Integer, 'sqlite'), ForeignKey('users.tg_user_id'), nullable=False) 
    timestamp = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
        
    user = relationship('User')