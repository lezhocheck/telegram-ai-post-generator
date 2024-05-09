from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from src.telegram.filters import PrivateChatFilter
from src.db.controllers import UserController, PostController
from aiogram.utils.chat_action import ChatActionSender
from src.schemas import (
    CreateUserSchema, 
    Conversation, 
    ConversationMessage, 
    CreatePostSchema,
    ResponsePostSchema
)
from src.inference.gpt import GptInferenceApi
from src.inference.dalle import DalleInferenceApi
from src.inference.whisper import WhisperInferenceApi
from src.telegram.utils import split_to_chunks
from typing import Optional
from io import BytesIO
from time import time


router = Router(name='telegram')

gpt_api = GptInferenceApi()
dalle_api = DalleInferenceApi()
whisper_api = WhisperInferenceApi()


NOT_SUPPORTED = '🥺 xBOT is currently supported only in private chats.'
GREETING_NEW = '👋 Hello, @{username}, welcome to xBOT!'
GREETING_OLD = '👋 Welcome back, @{username}!'
NEW_POST = "✅ Let's create new post. Send me text or audio with description."
ERROR_ON_GEN_IMAGE = '😕 Some error occured on image generation. Try one more time.'
ERROR_ON_MESSAGE = '😕 Some error occured on processing your request. Try one more time.'


@router.message(~PrivateChatFilter())
async def handle_not_private(message: Message) -> None:
    message.answer(NOT_SUPPORTED)


@router.message(PrivateChatFilter(), CommandStart())
async def command_start(message: Message) -> None:
    controller = UserController()
    user = message.from_user
    if controller.find_user(user.id):
        await message.answer(GREETING_OLD.format(username=user.username))
        return
    controller.create_user(CreateUserSchema(
        tg_user_id=user.id,
        tg_username=user.username,
        tg_chat_id=message.chat.id
    ))
    await message.answer(GREETING_NEW.format(username=user.username))


@router.message(PrivateChatFilter(), Command('post'))
async def start_new_post(message: Message) -> None:
    controller = PostController()
    controller.create_post(CreatePostSchema(
        tg_user_id=message.from_user.id,
        conversation=Conversation(messages=[])
    ))
    await message.answer(NEW_POST)


@router.message(PrivateChatFilter())
async def base_message(message: Message):
    async with ChatActionSender.typing(bot=message.bot, chat_id=message.chat.id):
        text = await get_message_text(message)
        if text is None:
            await message.answer(ERROR_ON_MESSAGE)
            return
        controller = PostController()
        id = message.from_user.id
        posts = controller.get_posts(id)
        if not len(posts):
            last_post = controller.create_post(CreatePostSchema(
                tg_user_id=message.from_user.id,
                conversation=Conversation(messages=[
                    ConversationMessage(role='user', content=text)
                ]
            )))
        else:
            last_post = controller.add_message(posts[0].post_id, ConversationMessage(
                role='user', 
                content=text
            ))
        await handle_post_message(message, last_post)


async def get_message_text(message: Message) -> Optional[str]:
    if message.voice is None:
        return message.text
    result: Optional[BytesIO] = await message.bot.download(message.voice)
    if result is None:
        return None
    result.name = f'{message.from_user.id}_{int(time())}.ogg'
    return await whisper_api.recognize(result)


async def handle_post_message(message: Message, post: ResponsePostSchema) -> None:
    controller = PostController()
    answer = await gpt_api.generate_post_text(post.conversation)
    controller.add_message(post.post_id, ConversationMessage(
        role='assistant', 
        content=answer
    ))
    generate_image = await gpt_api.is_image_asked(post.conversation)
    if not generate_image.image_required:
        for chunk in split_to_chunks(answer, 4096):
            await message.answer(chunk)
        return
    
    image = await dalle_api.generate_image(
        generate_image.prompt_for_text_to_image_model,
        output_name=f'{post.tg_user_id}_post_{post.post_id}.jpeg'
    )
    if not image:
        await message.answer(ERROR_ON_GEN_IMAGE)
        return
    
    splitted = split_to_chunks(answer, 1024, 4096)
    await message.answer_photo(image, caption=splitted[0])
    for chunk in splitted[1:]:
            await message.answer(chunk)
