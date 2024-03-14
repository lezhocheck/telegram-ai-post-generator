from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery
from aiogram.enums.chat_type import ChatType
from typing import Union


class PrivateChatFilter(Filter):    
    def __init__(self, *_) -> None:
        super().__init__()

    async def __call__(self, value: Union[Message, CallbackQuery]) -> bool:
        message = value
        if isinstance(value, CallbackQuery):
            message = value.message
        return message.chat.type == ChatType.PRIVATE
        