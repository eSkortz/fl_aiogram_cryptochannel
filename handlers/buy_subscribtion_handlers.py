from aiogram import Router, F
from aiogram.types import CallbackQuery, Message

from typing import Coroutine
from aiogram.types import FSInputFile

from keyboards import only_to_main, buying_subcribtion
from utils import database_utils

router = Router()


async def trial_approve(message: Message) -> Coroutine:
    markup_inline = buying_subcribtion.get(sub_type='trial')
    await message.delete()
    await message.answer('🔍 Уверены, что хотите приобрести подписку?', 
                         reply_markup=markup_inline) 
async def trial_failure(message: Message) -> Coroutine:
    markup_inline = only_to_main.get()
    await message.delete()
    await message.answer('❌ Вы уже активировали пробный период '\
                         'или у вас уже есть активная подписка', 
                         reply_markup=markup_inline)

async def light_approve(message: Message) -> Coroutine:
    markup_inline = buying_subcribtion.get(sub_type='light')
    await message.delete() 
    await message.answer('🔍 Уверены, что хотите приобрести подписку?', 
                         reply_markup=markup_inline)  
async def light_failure(message: Message) -> Coroutine:
    markup_inline = only_to_main.get()
    await message.delete()
    await message.answer('❌ У вас уже есть активная подписка '\
                         'или на вашем балансе недостаточно средств', 
                         reply_markup=markup_inline)

async def standard_approve(message: Message) -> Coroutine:
    markup_inline = buying_subcribtion.get(sub_type='standard')
    await message.delete() 
    await message.answer('🔍 Уверены, что хотите приобрести подписку?', 
                         reply_markup=markup_inline) 
async def standard_failure(message: Message) -> Coroutine:
    markup_inline = only_to_main.get()
    await message.delete()
    await message.answer('❌ У вас уже есть активная подписка '\
                         'или на вашем балансе недостаточно средств', 
                         reply_markup=markup_inline)

async def premium_approve(message: Message) -> Coroutine:
    markup_inline = buying_subcribtion.get(sub_type='premium')
    await message.delete() 
    await message.answer('🔍 Уверены, что хотите приобрести подписку?', 
                         reply_markup=markup_inline) 
async def premium_failure(message: Message) -> Coroutine:
    markup_inline = only_to_main.get()
    await message.delete()
    await message.answer('❌ У вас уже есть активная подписка '\
                         'или на вашем балансе недостаточно средств', 
                         reply_markup=markup_inline)


@router.callback_query(F.data == "buy_trial")
async def buy_trial(callback: CallbackQuery) -> Coroutine:
    is_have_trial = database_utils\
        .check_user_for_trial_subscribtion_by_user_id(user_id=callback.message.chat.id)
    is_have_active_subscribe = database_utils\
        .check_user_have_active_subcribtion(user_id=callback.message.chat.id)
    if not is_have_trial and not is_have_active_subscribe:
        await trial_approve(message=callback.message)
    else:
        await trial_failure(message=callback.message)

@router.callback_query(F.data == "buy_light")
async def buy_light(callback: CallbackQuery) -> Coroutine:
    is_have_active_subscribe = database_utils\
        .check_user_have_active_subcribtion(user_id=callback.message.chat.id)
    amount = database_utils.get_subscribtion_price_by_title(title='LIGHT')
    is_have_enough_money = database_utils\
        .check_user_have_enough_money(user_id=callback.message.chat.id, amount=amount)
    if is_have_enough_money and not is_have_active_subscribe:
        await light_approve(message=callback.message)
    else:
        await light_failure(message=callback.message)

@router.callback_query(F.data == "buy_standard")
async def buy_standard(callback: CallbackQuery) -> Coroutine:
    is_have_active_subscribe = database_utils\
        .check_user_have_active_subcribtion(user_id=callback.message.chat.id)
    amount = database_utils.get_subscribtion_price_by_title(title='LIGHT')
    is_have_enough_money = database_utils\
        .check_user_have_enough_money(user_id=callback.message.chat.id, amount=amount)
    if is_have_enough_money and not is_have_active_subscribe:
        await standard_approve(message=callback.message)
    else:
        await standard_failure(message=callback.message)

@router.callback_query(F.data == "buy_premium")
async def buy_premium(callback: CallbackQuery) -> Coroutine:
    is_have_active_subscribe = database_utils\
        .check_user_have_active_subcribtion(user_id=callback.message.chat.id)
    amount = database_utils.get_subscribtion_price_by_title(title='LIGHT')
    is_have_enough_money = database_utils\
        .check_user_have_enough_money(user_id=callback.message.chat.id, amount=amount)
    if is_have_enough_money and not is_have_active_subscribe:
        await premium_approve(message=callback.message)
    else:
        await premium_failure(message=callback.message)
    
    
@router.callback_query(F.data == "buying_trial")
async def buying_trial(callback: CallbackQuery) -> Coroutine:
    markup_inline = only_to_main.get()
    await callback.message.delete()
    await callback.message.answer('✅ Вы успешно приобрели подписку',
                                  reply_markup=markup_inline)
    database_utils.create_new_subscribtion(user_id=callback.message.chat.id,
                                           user_name=callback.message.chat.username,
                                           sub_type='TRIAL')


@router.callback_query(F.data == "buying_light")
async def buying_light(callback: CallbackQuery) -> Coroutine:
    markup_inline = only_to_main.get()
    await callback.message.delete()
    await callback.message.answer('✅ Вы успешно приобрели подписку',
                                  reply_markup=markup_inline)
    database_utils.create_new_subscribtion(user_id=callback.message.chat.id,
                                           user_name=callback.message.chat.username,
                                           sub_type='LIGHT')


@router.callback_query(F.data == "buying_standard")
async def buying_standard(callback: CallbackQuery) -> Coroutine:
    markup_inline = only_to_main.get()
    await callback.message.delete()
    await callback.message.answer('✅ Вы успешно приобрели подписку',
                                  reply_markup=markup_inline)
    database_utils.create_new_subscribtion(user_id=callback.message.chat.id,
                                           user_name=callback.message.chat.username,
                                           sub_type='STANDARD')


@router.callback_query(F.data == "buying_premium")
async def buying_premium(callback: CallbackQuery) -> Coroutine:
    markup_inline = only_to_main.get()
    await callback.message.delete()
    await callback.message.answer('✅ Вы успешно приобрели подписку',
                                  reply_markup=markup_inline)
    database_utils.create_new_subscribtion(user_id=callback.message.chat.id,
                                           user_name=callback.message.chat.username,
                                           sub_type='PREMIUM')