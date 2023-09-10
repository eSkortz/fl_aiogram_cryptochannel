from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import FSInputFile, Message

from keyboards.main import start
from utils import database_utils

from typing import Coroutine

router = Router()

@router.message(Command("start"))
async def start_command(message: Message) -> Coroutine:
    is_register = database_utils.Check.check_user_by_telegram_id(telegram_id=message.chat.id)
    if not is_register:
        database_utils.create_new_user(telegram_id=message.chat.id, username=message.chat.username)
    photo = FSInputFile("src/start.jpg")
    markup_inline = start.get(message.chat.id)
    await message.answer_photo(photo=photo, 
                                caption='🐍 Привет, я BitSnake бот, я могу помочь тебе ' \
                                'с оформлением подписки на канал BitSnake, а также ' \
                                'у меня есть функционал, который позволяет задать ' \
                                'интересующий тебя вопрос администраторам',
                                reply_markup=markup_inline)

@router.message(Command("recipient"))
async def recipient_command(message: Message) -> Coroutine:
    await message.reply(f"{message.chat.id}")
    

@router.message(Command("get_chat_info"))
async def get_chat_info(message: Message) -> Coroutine:
    await message.reply(f'{message}')