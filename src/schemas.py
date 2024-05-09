from pydantic import BaseModel, ConfigDict, BeforeValidator
from typing import Literal, List, Optional, Annotated, TypedDict
from datetime import datetime


class ConversationMessage(TypedDict):
    role: Literal['system', 'user', 'assistant']
    content: str


class Conversation(BaseModel):
    messages: List[ConversationMessage]


class CreateUserSchema(BaseModel):
    tg_user_id: int
    tg_username: str
    tg_chat_id: int


class ResponseUserSchema(CreateUserSchema):
    model_config = ConfigDict(from_attributes=True)
    
    is_active: bool
    joined_ts: datetime


class CreatePostSchema(BaseModel):
    tg_user_id: int
    conversation: Conversation


class ResponsePostSchema(CreatePostSchema):
    model_config = ConfigDict(from_attributes=True)

    post_id: int
    timestamp: datetime


class IsImageRequiredSchema(BaseModel):
    image_required: Annotated[bool, BeforeValidator(lambda x: bool(x))]
    prompt_for_text_to_image_model: Optional[str]