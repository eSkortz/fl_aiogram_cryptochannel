from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from typing import Coroutine, Optional

# * импортируем конфиг
from config.config_reader import bot_config
# * импортируем разметку
from keyboards.admin import only_to_admin
# * импортируем ручки под бд
from utils import database_utils

# * объявляем бота и роутер
bot = Bot(token=bot_config.TOKEN.get_secret_value())
router = Router()


class UserInfo(StatesGroup):
    waiting_for_username = State()


async def answer_for_userinfo_processing(message: Message, id_to_delete: int, user_info: Optional[dict or int]) -> Coroutine:
    """функция для вывода информации о пользователе из бд

    Args:
        message (Message): сообщение пользователя
        id_to_delete (int): id сообщения для подчистки чата
        user_info (Optional[dict or int]): словарь с информацией по пользователю
        или 0

    Returns:
        Coroutine: на выходе несколько корутин
    """
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
    """отработка колбэка на чек информации по пользователю

    Args:
        callback (CallbackQuery): сам колбэк
        state (FSMContext): наследуем fsm

    Returns:
        Coroutine: на выходе несколько корутин
    """
    await callback.message.delete()
    sent_message = await callback.message\
        .answer('✏️ Введите ник пользователя и отправьте его в чат')
    await state.set_state(UserInfo.waiting_for_username)
    await state.update_data(id = sent_message.message_id)
    

@router.message(UserInfo.waiting_for_username)
async def fsm_userinfo_processing(message: Message, state: FSMContext) -> Coroutine:
    """отработка состояния на ввод юзернейма

    Args:
        message (Message): сообщение пользователя
        state (FSMContext): наследуем fsm

    Returns:
        Coroutine: на выходе несколько корутин
    """
    user_info = database_utils.Get.get_all_user_info_by_username(username=message.text)
    state_data = await state.get_data()
    await answer_for_userinfo_processing(message=message, 
                                         id_to_delete=state_data['id'],
                                         user_info=user_info)
    