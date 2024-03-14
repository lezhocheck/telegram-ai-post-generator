from sqlalchemy.orm import Session
from ..controllers.post import PostController
from . import BaseController
from ..models.message import Message
from typing import Iterable, Dict, Any


class MessageController(BaseController):
    def __init__(self, db: Session, telegram_id: int) -> None:
        super().__init__(db, telegram_id)

    def add(self, data: Dict[str, Any] = None) -> Message:
        post_controller = PostController(self._db, self._telegram_id)
        post = post_controller.find_one(id=data['post_id'])
        message = Message(post=post, text=data['text'], type=data['type'])
        self._db.add(message)
        self._db.commit()
        return message
    
    def find_all(self, **filter_args: Dict[str, Any]) -> Iterable[Message]:
        return self._db.query(Message).filter_by(**filter_args).all()