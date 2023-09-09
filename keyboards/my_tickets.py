from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

from utils import database_utils

def get(user_id: int) -> ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    user_tickets = database_utils.get_five_tickets_by_user_id(user_id=user_id)
    # print(user_tickets)
    for i in range(len(user_tickets)):
        ticket_id = user_tickets[i][1]
        builder.row(types.InlineKeyboardButton(text=f'#{ticket_id} '\
                                               f'{user_tickets[i][0][:10]}', 
                                               callback_data=f'ticket_info|{ticket_id}'))
    builder.row(types.InlineKeyboardButton(
        text='🔙 В FAQ', callback_data='faq'
    ))
    return builder.as_markup(resize_keyboard=True)