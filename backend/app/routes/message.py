from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..connection import database
from ..models.message import Message
from ..schema import (
    MessageBase,
    MessageResponse
)
from typing import List, Iterable
from ..controllers.message import MessageController


router = APIRouter(prefix='/message')


@router.post('/', response_model=MessageResponse, status_code=200)
async def new_message(
    telegram_id: int, 
    data: MessageBase, 
    db: Session = Depends(database)
) -> Message:
    
    controller = MessageController(db, telegram_id)
    return controller.add(data.model_dump())


@router.get('/{post_id}', response_model=List[MessageResponse], status_code=200)
async def get_messages_of_post(
    telegram_id: int,
    post_id: int, 
    db: Session = Depends(database)
) -> Iterable[Message]:
    
    controller = MessageController(db, telegram_id)
    return controller.find_all(post_id=post_id)
