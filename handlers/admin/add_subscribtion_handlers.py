from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram import Bot

from typing import Coroutine, Optional

from config.config_reader import bot_config
from keyboards.admin import only_to_admin
from utils import database_utils


bot = Bot(token=bot_config.TOKEN.get_secret_value())

router = Router()


class AddSubcribtion(StatesGroup):
    waiting_for_username = State()
    waiting_for_days = State()
    

@router.callback_query(F.data == "add_days")
async def callback_add_days(callback: CallbackQuery, state: FSMContext) -> Coroutine:
    await callback.message.delete()
    sent_message = await callback.message\
        .answer('✏️ Введите ник пользователя и отправьте его в чат')
    await state.set_state(AddSubcribtion.waiting_for_username)
    await state.update_data(id = sent_message.message_id)
    

@router.message(AddSubcribtion.waiting_for_username)
async def fsm_adddays_processing_first(message: Message, state: FSMContext) -> Coroutine:
    is_user_with_username_exist = database_utils.Check.check_user_by_username(username=message.text)
    await message.delete()
    state_data = await state.get_data()
    await bot.delete_message(chat_id=message.chat.id, message_id=state_data['id'])
    if is_user_with_username_exist:
        sent_message = await message.answer('✏️ Отправьте кол-во дней, которое хотите добавить')
        await state.set_state(AddSubcribtion.waiting_for_days)
        await state.update_data(id = sent_message.message_id)
        await state.update_data(username = message.text)
    else:
        markup_inline = only_to_admin.get()
        await message.answer(text='❌ Проверьте правильность ввода', reply_markup=markup_inline)
        

@router.message(AddSubcribtion.waiting_for_days)
async def fsm_adddays_processing_second(message: Message, state: FSMContext) -> Coroutine:
    try:
        int(message.text)
    except Exception:
        days = False
    else:
        days = int(message.text)
    await message.delete()
    state_data = await state.get_data()
    await bot.delete_message(chat_id=message.chat.id, message_id=state_data['id'])
    markup_inline = only_to_admin.get()
    if days:
        username = state_data['username']
        database_utils.Create.create_service_subscribe(username=username, days=days)
        await message.answer('✅ Дни добавлены успешно', reply_markup=markup_inline)
    else:
        await message.answer(text='❌ Проверьте правильность ввода', reply_markup=markup_inline)