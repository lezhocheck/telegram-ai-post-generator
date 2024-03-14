from pydantic import BaseModel
from typing import Literal, List
from datetime import datetime


class ConversationMessage(BaseModel):
    role: Literal['system', 'user', 'assistant']
    content: str


class Conversation(BaseModel):
    messages: List[ConversationMessage]


class CreateUserSchema(BaseModel):
    tg_user_id: int
    tg_username: str
    tg_chat_id: int


class ResponseUserSchema(CreateUserSchema):
    is_active: bool
    joined_ts: datetime

    class Config:
        from_attributes = True


class CreatePostSchema(BaseModel):
    tg_user_id: int
    conversation: Conversation


class ResponsePostSchema(CreatePostSchema):
    post_id: int
    timestamp: datetime

    class Config:
        from_attributes = True
