# * разметка для создания одной кнопки возвращения в админ-панель
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

def get() -> ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text='🔙 Назад в админ-панель', callback_data="admin_panel"
    ))
    return builder.as_markup(resize_keyboard=True)