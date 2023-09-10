from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from typing import Coroutine

# * импортируем конфиг бота
from config.config_reader import bot_config
# * импортируем разметку
from keyboards.admin import approving_newsletter
# * импоритируем ручки под бд
from utils import database_utils
# * импортируем хендлер под главное меню
from handlers.main.commands import start_command

# * объявляем бота и роутер
bot = Bot(token=bot_config.TOKEN.get_secret_value())
router = Router()

# * класс для хранения состояний
class Newsletter(StatesGroup):
    waiting_for_text = State()
    

@router.callback_query(F.data == "sending_newsletter")
async def callback_create_newsletter(callback: CallbackQuery, state: FSMContext) -> Coroutine:
    """отработка колбэка под кнопку создать рассылку

    Args:
        callback (CallbackQuery): сам колбэк
        state (FSMContext): наследуем fsm

    Returns:
        Coroutine: на выходе несколько корутин
    """
    await callback.message.delete()
    state_data = await state.get_data()
    text = state_data['text']
    list_of_tgid = database_utils.Get.get_all_users_telegramid()
    await start_command(message=callback.message)
    for user_id in list_of_tgid:
        try:
            await bot.send_message(chat_id=user_id[0], text=text) 
        except Exception:
            continue


@router.callback_query(F.data == "create_newsletter")
async def callback_create_newsletter(callback: CallbackQuery, state: FSMContext) -> Coroutine:
    """отработка колбэка, отправка сообщение, установка состояния на ожидание
    текста рассылки от пользователя

    Args:
        callback (CallbackQuery): сам колбэк
        state (FSMContext): наслудуем fsm

    Returns:
        Coroutine: на выходе несколько корутин
    """
    await callback.message.delete()
    sent_message = await callback.message.answer('📨 Введите текст рассылки и отправьте его в чат')
    await state.set_state(Newsletter.waiting_for_text)
    await state.update_data(id = sent_message.message_id)
    

@router.message(Newsletter.waiting_for_text)
async def fsm_approving_text(message: Message, state: FSMContext) -> Coroutine:
    """отработка состояние на ввод текста рассылки

    Args:
        message (Message): сообщение пользователя
        state (FSMContext): наследуем fsm

    Returns:
        Coroutine: на выходе несколько корутин
    """
    markup_inline = approving_newsletter.get()
    text = message.text
    state_data = await state.get_data()
    await state.update_data(text = text)
    await bot.delete_message(chat_id=message.chat.id, message_id=state_data['id'])
    await message.delete()
    await message.answer(text=f'{text}\n\nВсе пользователи получат рассылку с таким текстом, '\
                        'уверены что хотите начать отправку?', reply_markup=markup_inline) 