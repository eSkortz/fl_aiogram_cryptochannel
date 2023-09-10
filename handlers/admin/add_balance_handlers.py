from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from typing import Coroutine

# * импортируем конфиг бота
from config.config_reader import bot_config
# * импортируем необходимую разметку
from keyboards.admin import only_to_admin
# * импортируем ручки к базе данных
from utils import database_utils

# * объявляем бота и роутер
bot = Bot(token=bot_config.TOKEN.get_secret_value())
router = Router()


class AddBalance(StatesGroup):
    """Класс стейтов, созданный для хранения состояния
    по вводу данных

    Args:
        StatesGroup (_type_): наследование дефолт класса
    """
    # * Стейт под ожидание ввода юзернейма
    waiting_for_username = State()
    # * Стейт под ожидание ввода суммы
    waiting_for_money = State()
    

@router.callback_query(F.data == "add_balance")
async def callback_add_balance(callback: CallbackQuery, state: FSMContext) -> Coroutine:
    """Отработка колбэка на пополнение баланса

    Args:
        callback (CallbackQuery): собственно сам колбэк и сообщение,
        с которого он прилетел
        state (FSMContext): наследуем fsm

    Returns:
        Coroutine: на выходе получаем несколько корутин
    """
    # * Удаляем сообщение, отправляем новое, ставим стейт и сохраняем в него id только
    # * только что отправленного сообщения
    await callback.message.delete()
    sent_message = await callback.message\
        .answer('✏️ Введите ник пользователя и отправьте его в чат')
    await state.set_state(AddBalance.waiting_for_username)
    await state.update_data(id = sent_message.message_id)
    

@router.message(AddBalance.waiting_for_username)
async def fsm_addbalance_processing_first(message: Message, state: FSMContext) -> Coroutine:
    """Отработка состояния, когда пользователь ввел username

    Args:
        message (Message): сообщение, которое прислал пользователь
        state (FSMContext): наследуем fsm

    Returns:
        Coroutine: на выходе получаем несколько корутин
    """
    # * Проверяем наличие пользователя с таким юзернеймом в базе данных
    is_user_with_username_exist = database_utils.Check.check_user_by_username(username=message.text)
    # * Удаляем сообщение, достаем данные из стейта, удаляем еще одно
    await message.delete()
    state_data = await state.get_data()
    await bot.delete_message(chat_id=message.chat.id, message_id=state_data['id'])
    # * Проверяем существование пользователя, в случае успеха переходим к следующему стейту
    if is_user_with_username_exist:
        sent_message = await message.answer('✏️ Отправьте сумму на которую хотите пополнить баланс пользователя')
        await state.set_state(AddBalance.waiting_for_money)
        await state.update_data(id = sent_message.message_id)
        await state.update_data(username = message.text)
    else:
        markup_inline = only_to_admin.get()
        await message.answer(text='❌ Проверьте правильность ввода', reply_markup=markup_inline)
        

@router.message(AddBalance.waiting_for_money)
async def fsm_addbalance_processing_second(message: Message, state: FSMContext) -> Coroutine:
    """Отработка состояния, когда пользователь ввел сумму

    Args:
        message (Message): сообщение пользователя
        state (FSMContext): наследуем fsm
    Returns:
        Coroutine: на выходе несколько корутин
    """
    # * Проверяем введено ли целочисленное значение
    try:
        int(message.text)
    except Exception:
        money = False
    else:
        money = int(message.text)
    # * Удаляем сообщения
    await message.delete()
    state_data = await state.get_data()
    await bot.delete_message(chat_id=message.chat.id, message_id=state_data['id'])
    markup_inline = only_to_admin.get()
    # * Если сумма введена корректно - обновляем баланс в бд
    if money:
        username = state_data['username']
        user_id = database_utils.Get.get_all_user_info_by_username(username=username)['telegram_id']
        database_utils.Update.update_user_balance_by_user_id(user_id=user_id, amount=money)
        await message.answer('✅ Баланс пользователя пополнен успешно', reply_markup=markup_inline)
    else:
        await message.answer(text='❌ Проверьте правильность ввода', reply_markup=markup_inline)