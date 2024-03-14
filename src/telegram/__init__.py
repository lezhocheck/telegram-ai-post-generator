from src.env import ENV
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
import logging
from aiogram.fsm.storage.memory import MemoryStorage
from src.telegram.handlers import router


bot = Bot(token=ENV.bot_token)
dispatcher = Dispatcher(storage=MemoryStorage())
dispatcher.include_router(router)


async def set_bot_commands() -> None:
    commands = [
        BotCommand(command='/start', description='👋 Start creating posts with me'),
        BotCommand(command='/post', description='Create new post')
    ]
    try:
        await bot.set_my_commands(commands)
    except Exception as e:
        logging.error(f'Cannot set commands: {e}')


async def setup_bot() -> None:
    webhook_info = await bot.get_webhook_info()
    expected_hook = f'https://{ENV.service_host}/telegram-hook'
    if webhook_info.url == expected_hook:
        return
    await bot.set_webhook(
        expected_hook,
        secret_token=ENV.telegram_secret
    )
    await set_bot_commands()
    