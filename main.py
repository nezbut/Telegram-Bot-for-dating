from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage, Redis
from aiogram.enums import ParseMode

from database import get_database, MongoDB

from motor.core import AgnosticDatabase
from config import Config
from language import getTranslator
from handlears import getRouters
from middlewares import TranslatorRunnerMiddleware, ReadyKeyboardsMiddleware, ViewFormsMiddleware
from fluentogram import TranslatorHub
from utils import set_menu_commands

import asyncio
import logging

logger = logging.getLogger(__name__)

async def main():
    redis = Redis()
    storage = RedisStorage(redis=redis)

    translator_hub: TranslatorHub = getTranslator()

    bot = Bot(token=Config.tg_bot.token, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=storage)
    database: AgnosticDatabase = get_database()
    mongo = MongoDB(db=database)

    dp.message.outer_middleware(TranslatorRunnerMiddleware())
    dp.message.middleware(ReadyKeyboardsMiddleware())
    dp.message.middleware(ViewFormsMiddleware())
    dp.callback_query.outer_middleware(TranslatorRunnerMiddleware())
    dp.callback_query.middleware(ReadyKeyboardsMiddleware())
    dp.callback_query.middleware(ViewFormsMiddleware())

    routers = getRouters()
    dp.include_routers(*routers)

    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("Drop old updates.")

    await set_menu_commands(bot=bot)

    logger.info("Bot start.")
    await dp.start_polling(bot, db=mongo, redis=redis, t_hub=translator_hub)

if __name__ == "__main__":

    if Config.tg_bot.bot_logs:
        logging.basicConfig(level=logging.INFO)

    asyncio.run(main())
