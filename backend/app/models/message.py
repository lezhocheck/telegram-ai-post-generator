from sqlalchemy import Column, DateTime, String, Integer, Enum, ForeignKey
from datetime import datetime
from . import BaseModel
from enum import StrEnum
from sqlalchemy.orm import relationship


class Type(StrEnum):
    SYSTEM = 'system'
    ASSISTANT = 'assistant'
    USER = 'user'


class Message(BaseModel):
    type = Column(Enum(Type, values_callable=lambda x: [e.value for e in x], name='type'), nullable=False)
    text = Column(String, nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'))
    post = relationship('Post', back_populates='messages')
    ts = Column(DateTime, default=datetime.utcnow(), nullable=False)