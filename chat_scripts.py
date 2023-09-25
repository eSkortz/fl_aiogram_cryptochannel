from aiogram import Bot
from typing import Coroutine
import datetime
import time
import asyncio

# * импортируем ручки для бд
from utils import database_utils
# * импортируем конфиг бота
from config.config_reader import bot_config

# * объявляем бота
bot = Bot(token=bot_config.TOKEN.get_secret_value())


async def auto_kicking_user() -> Coroutine:
    """функция для автоматического кика пользователей из чата.
    Отрабатывает раз в час.

    Returns:
        Coroutine: на выходе несколько корутин
    """
    while True:
        users = database_utils.Get.get_all_users_telegramid()
        for user in users:
            user_id = user[0]
            dateover = database_utils.Get.get_last_subscribtion_dateover_by_user_id(user_id=user_id)
            try:
                await bot.get_chat_member(chat_id=-1001975523437, user_id=user_id)
            except Exception:
                is_in_chat = False
            else:
                is_in_chat = True
            if datetime.datetime.now() > dateover and is_in_chat:
                await bot.ban_chat_member(chat_id=-1001975523437, user_id=user_id)
                await bot.unban_chat_member(chat_id=-1001975523437, user_id=user_id)
        await asyncio.sleep(3600)
        

async def auto_notify_user() -> Coroutine:
    """функция для автоматического увдомления пользователей, если
    до конца их подписки осталось меньше двух дней. Отрабатывает раз в сутки.

    Returns:
        Coroutine: на выходе несколько корутин
    """
    while True:
        users = database_utils.Get.get_all_users_telegramid()
        for user in users:
            user_id = user[0]
            dateover = database_utils.Get.get_last_subscribtion_dateover_by_user_id(user_id=user_id)
            if datetime.datetime.now() < dateover:
                time_diff = dateover - datetime.datetime.now()
                if time_diff.days < 2:
                    text = '🧨 Ваша подписка скоро закончится, не забудьте продлить её!'
                    await bot.send_message(chat_id=user_id, text=text) 
        await asyncio.sleep(86400)