import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram_dialog import setup_dialogs
from config_data.config import load_config
from aiogram.fsm.storage.redis import RedisStorage, Redis
import handlers.handlers
redis = Redis(host="localhost")

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s'
    )
    config = load_config()
    storage = RedisStorage(redis=redis)
    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher()
    dp.include_router(handlers.handlers.router)
    setup_dialogs(dp)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

asyncio.run(main())
