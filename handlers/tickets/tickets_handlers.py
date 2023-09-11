from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from typing import Coroutine

# * импортируем конфиг бота
from config.config_reader import bot_config
# * Импортируем ручки для бд
from utils import database_utils
# * Импортируем разметку
from keyboards.faq import my_tickets, ticket_info
from keyboards.main import only_to_main

# * Объявляем бота и роутер
bot = Bot(token=bot_config.TOKEN.get_secret_value())
router = Router()


class Ticket(StatesGroup):
    """класс для хранения состояний
    """
    waiting_new_ticket = State()


async def answer_for_request(message: Message, id_to_delete: int) -> Coroutine:
    """функция для выдачи сообщения после успешной регистрации тикета

    Args:
        message (Message): сообщение пользователя
        id_to_delete (int): id сообщения которое нужно будет подчистить

    Returns:
        Coroutine: на выходе несколько корутин
    """
    markup_inline = only_to_main.get()
    await message.delete()
    await bot.delete_message(chat_id=message.chat.id, message_id=id_to_delete)
    await message.answer('✅ Ваше обращение успешно зарегистрировано, вы можете ' \
                         'отслеживать его статус в разделе "🗂 Мои тикеты"', reply_markup=markup_inline)


@router.callback_query(F.data == "create_ticket")
async def create_ticket(callback: CallbackQuery, state: FSMContext) -> Coroutine:
    """отработка колбэка под создание тикета

    Args:
        callback (CallbackQuery): сам колбэк
        state (FSMContext): наследуем fsm 

    Returns:
        Coroutine: на выходе несколько корутин
    """
    await callback.message.delete()
    sent_message = await callback.message.answer('✏️ Введите свое обращение и отправьте его в чат')
    await state.set_state(Ticket.waiting_new_ticket)
    await state.update_data(id = sent_message.message_id)
    

@router.message(Ticket.waiting_new_ticket)
async def fsm_ticket_processing(message: Message, state: FSMContext) -> Coroutine:
    """отработка состояния ожидания ввода текста для тикета

    Args:
        message (Message): сообщение пользователя
        state (FSMContext): наследуем fsm

    Returns:
        Coroutine: на выходе несколько корутин
    """
    database_utils.Create.create_new_ticket(user_id=message.chat.id, username=message.chat.username, question=message.text)
    state_data = await state.get_data()
    await answer_for_request(message=message, id_to_delete=state_data['id'])


@router.callback_query(F.data == "my_tickets")
async def my_tickets_callback(callback: CallbackQuery) -> Coroutine:
    """отработка колбэка под раздел мои тикеты

    Args:
        callback (CallbackQuery): колбэк с сообщения

    Returns:
        Coroutine: на выходе несколкьо корутин
    """
    markup_inline = my_tickets.get(user_id=callback.message.chat.id)
    await callback.message.delete()
    await callback.message.answer('🗂 Это раздел мои тикеты, здесь хранятся '\
                                  'последние 5 ваших тикетов, по умолчанию поле '\
                                  'ответа пустое, оно заполнится, как только один из '\
                                  'администраторов ответит на ваш тикет', 
                                  reply_markup=markup_inline)


@router.callback_query(F.data.startswith('ticket_info'))
async def ticket_info_callback(callback: CallbackQuery):
    """отработка колбэка под информацию по конкретному тикету

    Args:
        callback (CallbackQuery): колбэк с сообщения
    """
    ticket_id = int(callback.data.split('|')[1])
    ticket_tuple = database_utils.Get.get_ticket_by_id(ticket_id=ticket_id)
    
    ticket_question = ticket_tuple[0]
    ticket_open = str(ticket_tuple[1])[:10]
    ticket_answer = ticket_tuple[2]
    ticket_close = str(ticket_tuple[3])[:10]

    markup_inline = ticket_info.get()
    await callback.message.delete()
    await callback.message.answer(text=f'Номер обращения - {ticket_id}\n\n' \
                                    f'Вопрос: {ticket_question}\n' \
                                    f'Дата открытия: {ticket_open}\n\n' \
                                    f'Ответ: {ticket_answer}\n' \
                                    f'Дата закрытия: {ticket_close}', 
                                    reply_markup=markup_inline)