from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

def get() -> ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text='💳 Купить подписку', callback_data="buy_trial"
    ))
    builder.row(types.InlineKeyboardButton(
        text='🔙 К подпискам', callback_data="subscribtions"
    ))
    return builder.as_markup(resize_keyboard=True)