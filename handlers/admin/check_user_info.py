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


class UserInfo(StatesGroup):
    waiting_for_username = State()


async def answer_for_userinfo_processing(message: Message, id_to_delete: int, user_info: Optional[dict or int]) -> Coroutine:
    markup_inline = only_to_admin.get()
    await message.delete()
    await bot.delete_message(chat_id=message.chat.id, message_id=id_to_delete)
    if user_info == 0:
        text = '❌ Кажется такого пользователя нет в базе данных, '\
            'проверьте корректность введенных вами данных и попробуйте '\
            'еще раз'
    else:
        text = ''
        for key in user_info.keys():
            text = text + f'{key} : {user_info[key]}\n'
    await message.answer(text=text, reply_markup=markup_inline)


@router.callback_query(F.data == "check_user")
async def callback_check_user(callback: CallbackQuery, state: FSMContext) -> Coroutine:
    await callback.message.delete()
    sent_message = await callback.message\
        .answer('✏️ Введите ник пользователя и отправьте его в чат')
    await state.set_state(UserInfo.waiting_for_username)
    await state.update_data(id = sent_message.message_id)
    

@router.message(UserInfo.waiting_for_username)
async def fsm_userinfo_processing(message: Message, state: FSMContext) -> Coroutine:
    user_info = database_utils.Get.get_all_user_info_by_username(username=message.text)
    state_data = await state.get_data()
    await answer_for_userinfo_processing(message=message, 
                                         id_to_delete=state_data['id'],
                                         user_info=user_info)
    