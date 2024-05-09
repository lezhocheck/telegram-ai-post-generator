from io import IOBase
import logging
import sys
from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.routes import router
from src.telegram import bot, setup_bot
from typing import AsyncGenerator, Optional
from src.db.controllers import db_manager


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator:
    db_manager.create_tables()
    await setup_bot()
    yield
    await bot.delete_webhook(drop_pending_updates=True)
    db_manager.close()


def init_logger(buffer: Optional[IOBase] = None) -> None:
    handlers = [logging.StreamHandler(sys.stdout)]
    if buffer is not None:
        handlers.append(logging.StreamHandler(buffer))
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=handlers
    )


def create_app() -> FastAPI:
    init_logger()
    app = FastAPI(
        title='xBOT',
        lifespan=lifespan
    )
    app.include_router(router)
    return app
