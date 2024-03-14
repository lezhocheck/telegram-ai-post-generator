from fastapi import FastAPI, APIRouter
from contextlib import asynccontextmanager
from .routes.chat import router as chat_router
from .routes.post import router as post_router
from .routes.message import router as message_router
from typing import Generator
from .state import StateManager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import BaseModel
import os


@asynccontextmanager
async def lifespan(_: FastAPI) -> Generator[None, None, None]:
    host = os.environ['POSTGRES_HOST']
    user = os.environ['POSTGRES_USER']
    password = os.environ['POSTGRES_PASSWORD']
    port = os.environ['POSTGRES_PORT']
    db = os.environ['POSTGRES_DB']
    db_url = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}'
    engine = create_engine(db_url)
    StateManager.SESSION = sessionmaker(
        autocommit=False, 
        autoflush=False, 
        bind=engine
    )
    BaseModel.metadata.create_all(bind=engine)
    yield
    StateManager.clear()


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    base_router = APIRouter(prefix='/{telegram_id}')
    base_router.include_router(chat_router)
    base_router.include_router(post_router)
    base_router.include_router(message_router)
    app.include_router(base_router)
    return app


app = create_app()