from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from typing import Coroutine

# * Импортируем конфиг бота
from config.config_reader import bot_config
# * Импортируем ручки под бд
from utils import database_utils
# * Импортируем разметку
from keyboards.admin import admin_tickets, admin_ticket_info, only_to_admin

# * объявляем бота и роутер
bot = Bot(token=bot_config.TOKEN.get_secret_value())
router = Router()

class Ticket(StatesGroup):
    waiting_for_response = State()
    

@router.callback_query(F.data == "admin_tickets")
async def callback_admin_tickets(callback: CallbackQuery) -> Coroutine:
    """отработка колбэка на список тикетов

    Args:
        callback (CallbackQuery): сам колюэк с сообщением

    Returns:
        Coroutine: на выходе несколько корутин
    """
    markup_inline = admin_tickets.get()
    await callback.message.delete()
    await callback.message.answer('🗂 Это раздел админ тикеты', 
                                  reply_markup=markup_inline)
    
    
@router.callback_query(F.data.startswith('admin_ticket_info'))
async def callback_admin_ticket_info(callback: CallbackQuery) -> Coroutine:
    """отработка колбэка под раздел информации по тикету
    в админ-панели

    Args:
        callback (CallbackQuery): сам колбэк

    Returns:
        Coroutine: на выходе несколько корутин
    """
    ticket_id = callback.data.split('|')[1]
    ticket_tuple = database_utils.Get.get_ticket_by_id(ticket_id=ticket_id)
    
    ticket_question = ticket_tuple[0]
    ticket_open = str(ticket_tuple[1])[:10]
    
    markup_inline = admin_ticket_info.get(ticket_id=ticket_id)
    await callback.message.delete()
    await callback.message.answer(text=f'Номер обращения - {ticket_id}\n\n' \
                                    f'Вопрос: {ticket_question}\n' \
                                    f'Дата открытия: {ticket_open}\n\n',
                                    reply_markup=markup_inline)
    
    
@router.callback_query(F.data.startswith('answer_for_ticket'))
async def callback_answer_for_ticket(callback: CallbackQuery, state: FSMContext) -> Coroutine:
    """отработка колюбэка под ответ на тикет

    Args:
        callback (CallbackQuery): сам колбэк
        state (FSMContext): наследуем fsm

    Returns:
        Coroutine: на выходе несколько корутин
    """
    ticket_id = callback.data.split('|')[1]
    sent_message = await callback.message.answer('✏️ Введите ответ и отправьте его в чат')
    await state.set_state(Ticket.waiting_for_response)
    await state.update_data(ticket_id = ticket_id, 
                            first_id = sent_message.message_id, 
                            second_id = callback.message.message_id)
            

@router.message(Ticket.waiting_for_response)
async def fsm_answer_for_ticket(message: Message, state: FSMContext) -> Coroutine:
    """отработка состояние на воод ответа на тикет

    Args:
        message (Message): сообщение пользователя
        state (FSMContext): наследуем fsm

    Returns:
        Coroutine: на выходе несколько корутин
    """
    state_data = await state.get_data()
    ticket_id = state_data['ticket_id']
    database_utils.Update.update_answer_for_ticket_by_id(ticket_id=ticket_id, answer=message.text)
    
    markup_inline = only_to_admin.get()
    await bot.delete_message(chat_id=message.chat.id, message_id=state_data['first_id']) 
    await bot.delete_message(chat_id=message.chat.id, message_id=state_data['second_id']) 
    await message.delete()
    await message.answer('✅ Ответ успешно записан', reply_markup=markup_inline)