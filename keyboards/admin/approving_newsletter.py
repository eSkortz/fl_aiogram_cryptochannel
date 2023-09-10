from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

def get() -> ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text='✅ Да', callback_data="sending_newsletter"
    ))
    builder.row(types.InlineKeyboardButton(
        text='❌ Нет', callback_data="admin_panel"
    ))
    return builder.as_markup(resize_keyboard=True)