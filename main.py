import asyncio
import logging
from aiogram import Bot, Dispatcher

from typing import Coroutine

from handlers import commands, main_handlers, subscribtions_handlers, wallet_handlers, buy_subscribtion_handlers, tickets_handlers
from config_reader import bot_config

logging.basicConfig(level=logging.INFO)
bot = Bot(token=bot_config.TOKEN.get_secret_value())
dp = Dispatcher()


async def main() -> Coroutine:
    dp.include_router(commands.router)
    dp.include_router(main_handlers.router)
    dp.include_router(subscribtions_handlers.router)
    dp.include_router(wallet_handlers.router)
    dp.include_router(buy_subscribtion_handlers.router)
    dp.include_router(tickets_handlers.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
    