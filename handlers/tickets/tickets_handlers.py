from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram import Bot

from typing import Coroutine

from config.config_reader import bot_config
from utils import database_utils

from keyboards.faq import my_tickets, ticket_info
from keyboards.main import only_to_main

bot = Bot(token=bot_config.TOKEN.get_secret_value())

router = Router()


class Ticket(StatesGroup):
    waiting_new_ticket = State()


async def answer_for_request(message: Message, id_to_delete: int) -> Coroutine:
    markup_inline = only_to_main.get()
    await message.delete()
    await bot.delete_message(chat_id=message.chat.id, message_id=id_to_delete)
    await message.answer('✅ Ваше обращение успешно зарегистрировано, вы можете ' \
                         'отслеживать его статус в разделе "🗂 Мои тикеты"', reply_markup=markup_inline)


@router.callback_query(F.data == "create_ticket")
async def create_ticket(callback: CallbackQuery, state: FSMContext) -> Coroutine:
    await callback.message.delete()
    sent_message = await callback.message.answer('✏️ Введите свое обращение и отправьте его в чат')
    await state.set_state(Ticket.waiting_new_ticket)
    await state.update_data(id = sent_message.message_id)
    

@router.message(Ticket.waiting_new_ticket)
async def fsm_ticket_processing(message: Message, state: FSMContext) -> Coroutine:
    database_utils.Create.create_new_ticket(user_id=message.chat.id, username=message.chat.username, question=message.text)
    state_data = await state.get_data()
    await answer_for_request(message=message, id_to_delete=state_data['id'])


@router.callback_query(F.data == "my_tickets")
async def my_tickets_callback(callback: CallbackQuery) -> Coroutine:
    markup_inline = my_tickets.get(user_id=callback.message.chat.id)
    await callback.message.delete()
    await callback.message.answer('🗂 Это раздел мои тикеты, здесь хранятся '\
                                  'последние 5 ваших тикетов, по умолчанию поле '\
                                  'ответа пустое, оно заполнится, как только один из '\
                                  'администраторов ответит на ваш тикет', 
                                  reply_markup=markup_inline)


@router.callback_query(F.data.startswith('ticket_info'))
async def ticket_info_callback(callback: CallbackQuery):
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