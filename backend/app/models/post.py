from sqlalchemy import Column, DateTime, ForeignKey, Integer
from datetime import datetime
from . import BaseModel
from sqlalchemy.orm import relationship


class Post(BaseModel):
    chat_id = Column(Integer, ForeignKey('chat.id'))
    chat = relationship('Chat', back_populates='posts', primaryjoin='Chat.id == Post.chat_id')
    messages = relationship('Message', back_populates='post')
    ts = Column(DateTime, default=datetime.utcnow(), nullable=False)