from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

def get() -> ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text='🛎 Тикеты', callback_data="none"
    ))
    builder.row(types.InlineKeyboardButton(
        text='📌 Добавить подписку пользователю', callback_data="none"
    ))
    builder.row(types.InlineKeyboardButton(
        text='📨 Создать рассылку', callback_data="none"
    ))
    builder.row(types.InlineKeyboardButton(
        text='🔙 Назад в главное меню', callback_data="main_menu"
    ))
    return builder.as_markup(resize_keyboard=True)