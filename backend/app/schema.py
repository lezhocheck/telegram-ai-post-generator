from pydantic import BaseModel
from datetime import datetime
from .models.message import Type
from .models.chat import Mode
from typing import List, Optional


class MessageBase(BaseModel):
    post_id: int
    type: Type
    text: str


class MessageResponse(MessageBase):
    id: int
    ts: datetime


class PostResponse(BaseModel):
    id: int
    chat_id: int
    messages: List[MessageResponse]
    ts: datetime


class ChatResponse(BaseModel):
    id: int
    created_ts: datetime
    mode: Mode
    current_post_id: Optional[int] = None


class UpdateChatModel(BaseModel):
    mode: Optional[Mode] = None
    current_post_id: Optional[int] = None
 