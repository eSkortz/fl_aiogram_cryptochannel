from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

def get() -> ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text='🪪 Инфа по пользователю', callback_data="check_user"
    ))
    builder.row(types.InlineKeyboardButton(
        text='📆 Добавить дни подписки пользователю', callback_data="add_days"
    ))
    builder.row(types.InlineKeyboardButton(
        text='💵 Пополнить счет пользователю', callback_data="add_balance"
    ))
    builder.row(types.InlineKeyboardButton(
        text='🛎 Тикеты', callback_data="admin_tickets"
    ))
    builder.row(types.InlineKeyboardButton(
        text='📨 Создать рассылку', callback_data="create_newsletter"
    ))
    builder.row(types.InlineKeyboardButton(
        text='🔙 В главное меню', callback_data="main_menu"
    ))
    return builder.as_markup(resize_keyboard=True)