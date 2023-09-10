from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.types import FSInputFile

from typing import Coroutine
import datetime

from keyboards.admin import admin
from keyboards.faq import faq
from keyboards.my_subscribtion import my_subscribtion
from keyboards.subscribtions import subscribtions
from keyboards.wallet import my_wallet
from keyboards.main import start

from utils import database_utils

router = Router()


@router.callback_query(F.data == "main_menu")
async def main_menu(callback: CallbackQuery) -> Coroutine:
    photo = FSInputFile("src/start.jpg")
    markup_inline = start.get(callback.message.chat.id)
    await callback.message.delete()
    await callback.message.answer_photo(photo=photo, 
                                        caption='🐍 Привет, я BitSnake бот, я могу помочь тебе ' \
                                        'с оформлением подписки на канал BitSnake, а также ' \
                                        'у меня есть функционал, который позволяет задать ' \
                                        'интересующий тебя вопрос администраторам',
                                        reply_markup=markup_inline)


@router.callback_query(F.data == "my_wallet")
async def my_wallet_callback(callback: CallbackQuery) -> Coroutine:
    markup_inline = my_wallet.get()
    balance = database_utils.Get.get_balance_by_telegram_id(telegram_id=callback.message.chat.id)
    username = callback.message.chat.username
    await callback.message.delete()
    await callback.message.answer(f'🪪 {username}\n\n' \
                                f'Баланс: {balance}$', 
                                reply_markup=markup_inline)
    
     
@router.callback_query(F.data == "subscribtions")
async def subscriptions_callback(callback: CallbackQuery) -> Coroutine:
    markup_inline = subscribtions.get()
    await callback.message.delete()
    await callback.message.answer(text='🛒 Доступные варианты подписки, период действия подписок ' \
                                        'не суммируется, пробная подписка доступна для активациии только 1 раз', 
                                        reply_markup=markup_inline)


@router.callback_query(F.data == "my_subscribtions")
async def my_subscription_callback(callback: CallbackQuery) -> Coroutine:
    markup_inline = my_subscribtion.get()
    date_over = database_utils.Get.get_last_subscribtion_dateover_by_user_id(user_id=callback.message.chat.id)
    if date_over > datetime.datetime.now():
        status = '✅ Active'
        timedifference = (date_over - datetime.datetime.now()).total_seconds()
    else:
        status = '❌ Inactive'
        timedifference = 0
    await callback.message.delete()
    await callback.message.answer('📈 Это раздел моя подписка, здесь вы можете ' \
                                    'посмотреть наличие активной подписки на вaшем ' \
                                    'аккаунте и кол-во дней до ее окончания\n\n' \
                                    f'Статус подписки: {status}\n\n' \
                                    f'⏱ До окончания: {int(timedifference // 86400)}d ' \
                                    f'{int((timedifference % 86400) // 3600)}h', 
                                    reply_markup=markup_inline)
    
    
@router.callback_query(F.data == "faq")
async def faq_callback(callback: CallbackQuery) -> Coroutine:
    markup_inline = faq.get()
    await callback.message.delete()
    await callback.message.answer(reply_markup=markup_inline, 
                                        text='💭 Это раздел помощи, здесь вы ' \
                                        'можете создать тикет и задать свой вопрос, ' \
                                        'мы ответим вам в ближайшее время')


@router.callback_query(F.data == "admin_panel")
async def admin_callback(callback: CallbackQuery) -> Coroutine:
    markup_inline = admin.get()
    await callback.message.delete()
    await callback.message.answer(reply_markup=markup_inline, 
                                  text='🔐 Это раздел администрирования, ' \
                                  'здесь можно ответить на тикет, ' \
                                  'начислить пользователю дни подписки или ' \
                                  'вывести информацию по пользователю ' \
                                  'или сделать рассылку для всех пользоветелей бота')
