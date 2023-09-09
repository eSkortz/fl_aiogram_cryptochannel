from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram import Bot

from typing import Coroutine

from utils import database_utils, tronscan_utils
from config_reader import bot_config
from keyboards import only_to_main

bot = Bot(token=bot_config.TOKEN.get_secret_value())

router = Router()


class Payment(StatesGroup):
    waiting_hash = State()


async def payment_success(message: Message, id_to_delete: int) -> Coroutine:
    markup_inline = only_to_main.get()
    await message.delete()
    await bot.delete_message(chat_id=message.chat.id, message_id=id_to_delete)
    await message.answer('✅ Ваш баланс пополнен', reply_markup=markup_inline)

async def payment_failure(message: Message, id_to_delete: int) -> Coroutine:
    markup_inline = only_to_main.get()
    await message.delete()
    await bot.delete_message(chat_id=message.chat.id, message_id=id_to_delete)
    await message.answer('❌ Что-то пошло не так', reply_markup=markup_inline)


@router.callback_query(F.data == 'payment')
async def payment(callback: CallbackQuery, state: FSMContext) -> Coroutine:
    await callback.message.delete()
    sent_message = await callback.message.answer('💳 Чтобы пополнить баланс переведите сумму, ' \
        f'которую хотите внести на адрес:\n\n{bot_config.USDT_WALLET}\n\nПосле этого пришлите ' \
        'следующим сообщением hash транзакции, после чего программа автоматически ' \
        'проверит статус платежа и зачислит деньги на ваш баланс')
    await state.set_state(Payment.waiting_hash)
    await state.update_data(id = sent_message.message_id)
    

@router.message(Payment.waiting_hash)
async def payment_processing(message: Message, state: FSMContext) -> Coroutine:
    hash = message.text
    result, amount = tronscan_utils.check_transaction_by_hash(hash)
    state_data = await state.get_data()
    if result:
        status = True
        await payment_success(message, state_data['id'])
    else:
        status = False
        await payment_failure(message, state_data['id'])
    database_utils.create_new_transaction(hash=hash, amount=amount, from_user_id=message.chat.id, status = status)
    