"""разметка под раздел админ тикетов
"""
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

from utils import database_utils

def get() -> ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    empty_tickets = database_utils.Get.get_all_empty_tickets()
    # print(user_tickets)
    for i in range(len(empty_tickets)):
        ticket_id = empty_tickets[i][1]
        builder.row(types.InlineKeyboardButton(text=f'#{ticket_id} '\
                                               f'{empty_tickets[i][0][:10]}', 
                                               callback_data=f'admin_ticket_info|{ticket_id}'))
    builder.row(types.InlineKeyboardButton(
        text='🔙 В админ-панель', callback_data='admin_panel'
    ))
    return builder.as_markup(resize_keyboard=True)
