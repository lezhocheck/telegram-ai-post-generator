from sqlalchemy.orm import Session
from . import BaseController
from ..models.chat import Chat
from typing import Dict, Any, Iterable, Optional


class ChatController(BaseController):
    def __init__(self, db: Session, telegram_id: int) -> None:
        super().__init__(db, telegram_id)

    def add(self, data: Optional[Dict[str, Any]] = None) -> Chat:
        if data is None:
            chat = Chat(telegram_id=self._telegram_id)
        else:
            chat = Chat(**data)
        self._db.add(chat)
        self._db.commit()
        return chat
    
    def find_all(self, **filter_args: Dict[str, Any]) -> Iterable[Chat]:
        return self._db.query(Chat).filter_by(**filter_args).all()