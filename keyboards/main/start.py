from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

admins = [5408815987, 260871716]

def get(user_id: int) -> ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text='🪪 Мой кошелек', callback_data="my_wallet"
    ))
    builder.row(types.InlineKeyboardButton(
        text='🛒 Подписки', callback_data="subscribtions"
    ), types.InlineKeyboardButton(
        text='📈 Моя подписка', callback_data="my_subscribtions"
    ))
    builder.row(types.InlineKeyboardButton(
        text='💭 FAQ', callback_data="faq"
    ))
    if user_id in admins:
        builder.row(types.InlineKeyboardButton(
            text='🔐 Админ панель', callback_data="admin_panel"
        ))
    return builder.as_markup(resize_keyboard=True)