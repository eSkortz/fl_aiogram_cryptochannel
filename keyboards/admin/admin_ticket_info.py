from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

def get(ticket_id: int) -> ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text='📝 Ответить на тикет', 
        callback_data=f'answer_for_ticket|{ticket_id}'
    ))
    builder.row(types.InlineKeyboardButton(
        text='🔙 В тикеты', callback_data='admin_tickets'
    ))
    return builder.as_markup(resize_keyboard=True)