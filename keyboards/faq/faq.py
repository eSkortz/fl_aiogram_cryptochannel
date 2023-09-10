from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

def get() -> ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text='✏️ Создать тикет', callback_data="create_ticket"
        ),
        types.InlineKeyboardButton(
            text='🗂 Мои тикеты', callback_data="my_tickets"
        )
    )
    builder.row(types.InlineKeyboardButton(
        text='🔙 В главное меню', callback_data="main_menu"
    ))
    return builder.as_markup(resize_keyboard=True)