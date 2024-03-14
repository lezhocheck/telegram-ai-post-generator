from fastapi import APIRouter, Request, Response, HTTPException
from http import HTTPStatus
from src.env import ENV
from aiogram.types import Update
from src.telegram import bot, dispatcher


router = APIRouter()


@router.post('/telegram-hook')
async def bot_webhook(request: Request) -> Response:
    secret = request.headers.get('x-telegram-bot-api-secret-token')
    if secret != ENV.telegram_secret:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, 
            detail='Invalid secret token.'
        )
    data = await request.json()
    update = Update(**data)
    await dispatcher.feed_update(bot=bot, update=update)
    return Response(status_code=HTTPStatus.OK)