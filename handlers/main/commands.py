"""файл для отработки команд в боте
"""
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import FSInputFile, Message
from typing import Coroutine

# * импортируем разметку
from keyboards.main import start
# * импортируем ручки под бд
from utils import database_utils
# * импортируем конфиг бота
from config.config_reader import bot_config

# * объявляем роутер
router = Router()

@router.message(Command("start"))
async def start_command(message: Message) -> Coroutine:
    """отработка команды /start

    Args:
        message (Message): сообщение пользователя

    Returns:
        Coroutine: на выходе несколько корутин
    """
    # * проверяем существует ли такой пользователь в базе данных
    is_register = database_utils.Check.check_user_by_telegram_id(telegram_id=message.chat.id)
    # * если нет - регистрируем
    if not is_register:
        database_utils.Create.create_new_user(telegram_id=message.chat.id, username=message.chat.username)
    photo = FSInputFile("src/start.jpg")
    markup_inline = start.get(message.chat.id)
    await message.answer_photo(photo=photo, 
                                caption='🐍 Привет, я BitSnake бот, я могу помочь тебе ' \
                                'с оформлением подписки на канал BitSnake, а также ' \
                                'у меня есть функционал, который позволяет задать ' \
                                'интересующий тебя вопрос администраторам',
                                reply_markup=markup_inline)

# @router.message(Command("recipient"))
# async def recipient_command(message: Message) -> Coroutine:
#     await message.reply(f"{message.chat.id}")
    

# @router.message(Command("get_chat_info"))
# async def get_chat_info(message: Message) -> Coroutine:
#     await message.reply(f'{message}')