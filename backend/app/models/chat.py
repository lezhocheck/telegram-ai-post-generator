from enum import StrEnum
from sqlalchemy import Column, DateTime, Enum, Integer, ForeignKey
from datetime import datetime
from . import BaseModel
from sqlalchemy.orm import relationship


class Mode(StrEnum):
    WRITE_TEXT = 'write_text'
    GENERATE_IMAGE = 'gen_image'


class Chat(BaseModel):
    telegram_id = Column(Integer, nullable=False, index=True, unique=True)
    posts = relationship('Post', back_populates='chat', primaryjoin='Chat.id == Post.chat_id')
    created_ts = Column(DateTime, default=datetime.utcnow(), nullable=False)
    mode = Column(Enum(
        Mode, 
        values_callable=lambda x: [e.value for e in x], name='role'), 
        nullable=False, 
        default=Mode.WRITE_TEXT
    )
    current_post_id = Column(Integer, ForeignKey('post.id'), nullable=True)


