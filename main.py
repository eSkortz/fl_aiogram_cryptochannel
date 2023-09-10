import asyncio
import logging
from aiogram import Bot, Dispatcher

from typing import Coroutine

from chat_scripts import auto_kicking_user, auto_notify_user

# * Импортируем значения из конфига
from config.config_reader import bot_config

# * Импортируем все хендлеры
from handlers.main import commands, main_handlers
from handlers.wallet import wallet_handlers
from handlers.subscribtions import buy_subscribtion_handlers, subscribtions_handlers
from handlers.tickets import tickets_handlers
from handlers.admin import check_user_info, add_subscribtion_handlers,\
    create_newsletter, admin_tickets_handlers, add_balance_handlers

# * Настраиваем логирование, обьявляем бота и диспетчер
logging.basicConfig(level=logging.INFO)
bot = Bot(token=bot_config.TOKEN.get_secret_value())
dp = Dispatcher()


async def main() -> Coroutine:
    
    # * Включаем в диспетчер роутеры главного меню и команд
    dp.include_routers(commands.router, 
                       main_handlers.router)
    
    # * Включаем в диспетчер роутеры раздела кошелек
    dp.include_router(wallet_handlers.router)
    
    # * Включаем в диспетчер роутеры раздела подписок
    dp.include_routers(subscribtions_handlers.router, 
                       buy_subscribtion_handlers.router)
    
    # * Включаем в диспетчер роутеры раздела мои подписки
    dp.include_router(tickets_handlers.router)
    
    # * Включаем в диспетчер роутеры раздела админ-панели
    dp.include_routers(check_user_info.router, 
                       add_subscribtion_handlers.router,
                       add_balance_handlers.router,
                       create_newsletter.router,
                       admin_tickets_handlers.router)
    
    # * Пропускаем все накопившиеся соообщения
    await bot.delete_webhook(drop_pending_updates=True)
    
    # * Запускаем поллинг бота
    await asyncio.create_task(dp.start_polling(bot))
    #await asyncio.create_task(auto_notify_user())
    #await asyncio.create_task(auto_kicking_user())


if __name__ == "__main__":
    asyncio.run(main())
    