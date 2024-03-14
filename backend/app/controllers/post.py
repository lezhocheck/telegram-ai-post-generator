from sqlalchemy.orm import Session
from ..controllers.chat import ChatController
from . import BaseController
from ..models.post import Post
from typing import Dict, Any, Iterable


class PostController(BaseController):
    def __init__(self, db: Session, telegram_id: int) -> None:
        super().__init__(db, telegram_id)

    def add(self, _: Dict[str, Any] = None) -> Post:
        chat_controller = ChatController(self._db, self._telegram_id)
        chat = chat_controller.get(telegram_id=self._telegram_id)
        post = Post(chat=chat)
        self._db.add(post)
        self._db.commit()
        return post
    
    def find_all(self, **filter_args: Dict[str, Any]) -> Iterable[Post]:
        return self._db.query(Post).filter_by(**filter_args).all()