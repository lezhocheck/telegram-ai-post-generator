from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..connection import database
from ..models.chat import Chat
from ..schema import ChatResponse, UpdateChatModel
from ..controllers.chat import ChatController


router = APIRouter(prefix='/chat')


@router.post('/', response_model=ChatResponse, status_code=200)
async def new_chat(
    telegram_id: int, 
    db: Session = Depends(database)
) -> Chat:
    
    chat_controller = ChatController(db, telegram_id)
    if chat_controller.exists(telegram_id=telegram_id):
        raise HTTPException(status_code=400, detail='Chat already exists')
    return chat_controller.add()


@router.get('/', response_model=ChatResponse, status_code=200)
async def get_chat(
    telegram_id: int, 
    db: Session = Depends(database)
) -> Chat:
    
    chat_controller = ChatController(db, telegram_id)
    chat = chat_controller.find_one(telegram_id=telegram_id)
    if chat is None:
        raise HTTPException(status_code=400, detail='Chat does not exist')
    return chat


@router.patch('/', response_model=ChatResponse, status_code=200)
async def update_chat(
    telegram_id: int, 
    data: UpdateChatModel, 
    db: Session = Depends(database)
) -> Chat:
    
    chat_controller = ChatController(db, telegram_id)
    chat = chat_controller.find_one(telegram_id=telegram_id)
    if chat is None:
        raise HTTPException(status_code=400, detail='Chat does not exist')
    return chat_controller.update(chat.id, data.model_dump())