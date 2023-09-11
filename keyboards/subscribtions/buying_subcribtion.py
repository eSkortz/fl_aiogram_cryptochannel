# * разметка для сообщения подтверждения покупки подписки
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

def get(sub_type) -> ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text='✅ Да', callback_data=f'buying|{sub_type}'
    ), types.InlineKeyboardButton(
        text='❌ Нет', callback_data="subcribtions"
    ))
    return builder.as_markup(resize_keyboard=True)
    