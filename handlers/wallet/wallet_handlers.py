from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram import Bot

import datetime
from typing import Coroutine

from config.config_reader import bot_config
from utils import database_utils, tronscan_utils

from keyboards.wallet import payment_keyboard
from keyboards.main import only_to_main

bot = Bot(token=bot_config.TOKEN.get_secret_value())

router = Router()


class Payment(StatesGroup):
    waiting_hash = State()    
    waiting_processing = State()

async def payment_success(message: Message) -> Coroutine:
    markup_inline = only_to_main.get()
    await message.delete()
    await message.answer('✅ Ваш баланс пополнен', reply_markup=markup_inline)

async def payment_failure(message: Message) -> Coroutine:
    markup_inline = only_to_main.get()
    await message.delete()
    await message.answer('❌ Что-то пошло не так', reply_markup=markup_inline)
    

async def payment_processing(message: Message, hash: str) -> Coroutine:
    result, amount = tronscan_utils.check_transaction_by_hash(hash)
    if result:
        database_utils.Update.update_transaction_by_hash(hash=hash, amount=amount, date=datetime.datetime.now())
        database_utils.Update.update_user_balance_by_user_id(user_id=message.chat.id, amount=amount)
        await payment_success(message=message)
    else:
        markup_inline = payment_keyboard.get(hash=hash)
        await message.delete()
        text = 'Мы обрабатываем ваш платеж, нажмите '\
               'кнопку как только будете уверен что платеж прошел, '\
               'после этого деньги автоматически зачислятся на ваш баланс'
        await message.answer(text=text, reply_markup=markup_inline)


@router.callback_query(F.data.startswith('payment_processing'))
async def callback_payment_processing(callback: CallbackQuery) -> Coroutine:
    hash = callback.data.split('|')[1]
    result, amount = tronscan_utils.check_transaction_by_hash(hash)
    if result:
        database_utils.Update.update_transaction_by_hash(hash=hash, amount=amount, date=datetime.datetime.now())
        database_utils.Update.update_user_balance_bu_user_id(user_id=callback.message.chat.id, amount=amount)
        await payment_success(message=callback.message)
    else:
        markup_inline = payment_keyboard.get(hash=hash)
        await callback.message.delete()
        text = 'Мы обрабатываем ваш платеж, нажмите '\
               'кнопку как только будете уверен что платеж прошел, '\
               'после этого деньги автоматически зачислятся на ваш баланс'
        await callback.message.answer(text=text, reply_markup=markup_inline)


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
async def payment_wait(message: Message, state: FSMContext) -> Coroutine:
    hash = message.text
    await state.update_data(hash = hash)
    is_exist_transaction = database_utils.Check.check_transactions_by_hash(hash=hash)
    
    state_data = await state.get_data()
    id_to_delete = state_data['id']
    await bot.delete_message(chat_id=message.chat.id, message_id=id_to_delete)

    result, amount = tronscan_utils.check_transaction_by_hash(hash)
    
    if is_exist_transaction:
        await payment_failure(message)
    elif result:
        database_utils.Create.create_new_transaction(hash=hash, from_user_id=message.chat.id, amount=amount, status=True, date=datetime.datetime.now())
        database_utils.Update.update_user_balance_by_user_id(user_id=message.chat.id, amount=amount)
        await payment_success(message=message)
    else:
        database_utils.Create.create_new_transaction(hash=hash, from_user_id=message.chat.id)
        await payment_processing(message=message, hash=hash)