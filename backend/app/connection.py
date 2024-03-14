from typing import Generator
from .state import StateManager
from sqlalchemy.orm import Session


def database() -> Generator:
    db: Session = StateManager.SESSION()
    try:
        yield db
    finally:
        db.close()