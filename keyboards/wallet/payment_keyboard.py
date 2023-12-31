# * разметка для сообщения проверки пополнения
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

def get(hash) -> ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text='♻️ Обновить данные', callback_data=f'payment_processing|{hash}'
    ))
    return builder.as_markup(resize_keyboard=True)