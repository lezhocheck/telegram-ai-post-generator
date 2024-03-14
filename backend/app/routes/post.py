from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..connection import database
from ..models.post import Post
from ..controllers.post import PostController
from ..controllers.chat import ChatController
from ..schema import PostResponse
from typing import List


router = APIRouter(prefix='/post')


@router.post('/', response_model=PostResponse, status_code=200)
async def new_post(telegram_id: int, db: Session = Depends(database)) -> Post:
    post_controller = PostController(db, telegram_id)
    return post_controller.add()


@router.get('/', response_model=List[PostResponse], status_code=200)
async def get_posts(telegram_id: int, db: Session = Depends(database)) -> List[Post]:
    post_controller = PostController(db, telegram_id)
    return post_controller.find_all(chat_id=telegram_id)


@router.get('/current', response_model=PostResponse, status_code=200)
async def current_post(telegram_id: int, db: Session = Depends(database)) -> Post:
    chat_controller = ChatController(db, telegram_id)
    post_controller = PostController(db, telegram_id)
    current_chat = chat_controller.find_one(telegram_id=telegram_id)
    return post_controller.get(id=current_chat.current_post_id)