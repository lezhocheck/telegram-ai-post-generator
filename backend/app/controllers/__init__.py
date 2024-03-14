from fastapi import HTTPException
from sqlalchemy.orm import Session
from abc import ABCMeta, abstractmethod
from typing import TypeVar, Iterable, Dict, Any, Optional
from ..models import BaseModel
from sqlalchemy.exc import IntegrityError


Model = TypeVar('Model', bound=BaseModel)


class BaseController(metaclass=ABCMeta):
    def __init__(self, db: Session, telegram_id: int) -> None:
        self._db = db
        self._telegram_id = telegram_id
    
    @abstractmethod
    def add(self, data: Optional[Dict[str, Any]] = None) -> Model:
        raise NotImplementedError()
    
    @abstractmethod
    def find_all(self, **filter_args: Dict[str, Any]) -> Iterable[Model]:
        return NotImplementedError()
    
    def find_one(self, **filter_args: Dict[str, Any]) -> Optional[Model]:
        return next(iter(self.find_all(**filter_args)), None)
    
    def exists(self, **filter_args: Dict[str, Any]) -> bool:
        return self.find_one(**filter_args) is not None
    
    def get(self, **filter_args: Dict[str, Any]) -> Model:
        item = self.find_one(**filter_args)
        if item is None:
            name = item.__class__.__name__
            raise HTTPException(status_code=400, detail=f'{name} not found')
        return item
    
    def update(self, id: int, data: Dict[str, Any]) -> Model:
        item = self.get(id=id)
        for key, value in data.items():
            if value is not None:
                setattr(item, key, value)
        try:
            self._db.commit()
        except IntegrityError:
            name = item.__class__.__name__
            raise HTTPException(status_code=400, detail=f'Invalid {name} provided')
        return item