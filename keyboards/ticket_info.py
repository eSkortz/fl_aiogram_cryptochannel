from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

from utils import database_utils

def get() -> ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text='🔙 В мои тикеты', callback_data='my_tickets'
    ))
    return builder.as_markup(resize_keyboard=True)