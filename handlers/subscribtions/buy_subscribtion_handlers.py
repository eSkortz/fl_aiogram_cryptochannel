from aiogram import Router, F
from aiogram.types import CallbackQuery, Message

from typing import Coroutine

from keyboards.main import only_to_main
from keyboards.subscribtions import buying_subcribtion
from utils import database_utils

router = Router()


async def buying_approve(message: Message, sub_type: str) -> Coroutine:
    markup_inline = buying_subcribtion.get(sub_type=sub_type)
    await message.delete()
    await message.answer('🔍 Уверены, что хотите приобрести подписку?', 
                         reply_markup=markup_inline) 
    

async def buying_failure(message: Message) -> Coroutine:
    markup_inline = only_to_main.get()
    await message.delete()
    await message.answer('❌ На вашем балансе недостаточно средств '\
                        '(или вы уже активировали пробный период)', 
                         reply_markup=markup_inline)


@router.callback_query(F.data == "buy_trial")
async def callback_buy_trial(callback: CallbackQuery) -> Coroutine:
    is_have_trial = database_utils.Check\
        .check_user_for_trial_subscribtion_by_user_id(user_id=callback.message.chat.id)
    is_have_subscribtions = database_utils.Check\
        .check_subcription_by_user_id(user_id=callback.message.chat.id)
    if not is_have_trial and not is_have_subscribtions:
        await buying_approve(message=callback.message, sub_type='TRIAL')
    else:
        await buying_failure(message=callback.message)

@router.callback_query(F.data == "buy_light")
async def callback_buy_light(callback: CallbackQuery) -> Coroutine:
    amount = database_utils.Get.get_subscribtion_price_by_title(title='LIGHT')
    is_have_enough_money = database_utils.Check\
        .check_user_have_enough_money(user_id=callback.message.chat.id, amount=amount)
    if is_have_enough_money:
        await buying_approve(message=callback.message, sub_type='LIGHT')
    else:
        await buying_failure(message=callback.message)

@router.callback_query(F.data == "buy_standard")
async def callback_buy_standard(callback: CallbackQuery) -> Coroutine:
    amount = database_utils.Get.get_subscribtion_price_by_title(title='LIGHT')
    is_have_enough_money = database_utils.Check\
        .check_user_have_enough_money(user_id=callback.message.chat.id, amount=amount)
    if is_have_enough_money:
        await buying_approve(message=callback.message, sub_type='STANDARD')
    else:
        await buying_failure(message=callback.message)

@router.callback_query(F.data == "buy_premium")
async def callback_buy_premium(callback: CallbackQuery) -> Coroutine:
    amount = database_utils.Get.get_subscribtion_price_by_title(title='LIGHT')
    is_have_enough_money = database_utils.Check\
        .check_user_have_enough_money(user_id=callback.message.chat.id, amount=amount)
    if is_have_enough_money:
        await buying_approve(message=callback.message, sub_type='PREMIUM')
    else:
        await buying_failure(message=callback.message)


@router.callback_query(F.data.startswith('buying|'))
async def callback_buying_subcribtion(callback: CallbackQuery) -> Coroutine:
    sub_title = callback.data.split('|')[1]
    is_have_active_subscribtion = database_utils.Check\
        .check_user_have_active_subcribtion(user_id=callback.message.chat.id)
    if is_have_active_subscribtion:
        sub_id = database_utils.Get\
            .get_last_subscribtion_id_by_user_id(user_id=callback.message.chat.id)
        days = database_utils.Get\
            .get_subscribtion_days_by_title(title=sub_title)
        database_utils.Update.update_subscription_for_ndays(sub_id=sub_id, days=days)
    else:
        database_utils.Create\
            .create_new_subscribtion(user_id=callback.message.chat.id,
                                     user_name=callback.message.chat.username,
                                     sub_type=sub_title)
    markup_inline = only_to_main.get()
    await callback.message.delete()
    await callback.message.answer('✅ Вы успешно приобрели подписку',
                                  reply_markup=markup_inline)