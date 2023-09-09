from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

from utils import database_utils

def get() -> ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    days_trial = database_utils.get_subscribtion_days_by_title(title='TRIAL')
    
    days_light = database_utils.get_subscribtion_days_by_title(title='LIGHT')
    price_light = database_utils.get_subscribtion_price_by_title(title='LIGHT')
    
    days_standard = database_utils.get_subscribtion_days_by_title(title='STANDARD')
    price_standard = database_utils.get_subscribtion_price_by_title(title='STANDARD')
    
    days_premium = database_utils.get_subscribtion_days_by_title(title='PREMIUM')
    price_premium = database_utils.get_subscribtion_price_by_title(title='PREMIUM')
    
    builder.row(types.InlineKeyboardButton(
        text=f'📙 Bitsnake Trial ({days_trial} days) - Free', 
        callback_data="subscribtion_trial"
        ))
    builder.row(types.InlineKeyboardButton(
        text=f'📗 Bitsnake Light ({days_light} days) - {price_light}$', 
        callback_data="subscribtion_light"
        ))
    builder.row(types.InlineKeyboardButton(
        text=f'📕 Bitsnake Standard ({days_standard} days) - {price_standard}$', 
        callback_data="subscribtion_standard"
        ))
    builder.row(types.InlineKeyboardButton(
        text=f'📘 Bitsnake Premium ({days_premium} days) - {price_premium}$', 
        callback_data="subscribtion_premium"
        ))
    builder.row(types.InlineKeyboardButton(
        text='🔙 Назад в главное меню', callback_data="main_menu"
    ))
    return builder.as_markup(resize_keyboard=True)