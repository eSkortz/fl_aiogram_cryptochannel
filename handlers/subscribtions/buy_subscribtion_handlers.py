from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message
from typing import Coroutine

# * импортируем разметку
from keyboards.main import only_to_main
from keyboards.subscribtions import buying_subcribtion
# * импортируем ручки под бд
from utils import database_utils
# * импортируем конфиг
from config.config_reader import bot_config

# * объявляем бота и роутер
bot = Bot(token=bot_config.TOKEN.get_secret_value())
router = Router()


async def buying_approve(message: Message, sub_type: str) -> Coroutine:
    """функция на подтверждение покупки подписки

    Args:
        message (Message): сообщение пользователя
        sub_type (str): тип подписки

    Returns:
        Coroutine: на выходе несколько корутин
    """
    markup_inline = buying_subcribtion.get(sub_type=sub_type)
    await message.delete()
    await message.answer('🔍 Уверены, что хотите приобрести подписку?', 
                         reply_markup=markup_inline) 
    

async def buying_failure(message: Message) -> Coroutine:
    """функция на отказ по покупке подписки

    Args:
        message (Message): сообщение пользователя

    Returns:
        Coroutine: на выходе несколько корутин
    """
    markup_inline = only_to_main.get()
    await message.delete()
    await message.answer('❌ На вашем балансе недостаточно средств '\
                        '(или вы уже активировали пробный период)', 
                         reply_markup=markup_inline)


@router.callback_query(F.data == "buy_trial")
async def callback_buy_trial(callback: CallbackQuery) -> Coroutine:
    """отработка колбэка на покупку подписки типа trial

    Args:
        callback (CallbackQuery): колбэк с сообщения

    Returns:
        Coroutine: на выходе несколько корутин
    """
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
    """отработка колбэка на покупку подписки типа light

    Args:
        callback (CallbackQuery): колбэк с сообщения

    Returns:
        Coroutine: на выходе несколько корутин
    """
    amount = database_utils.Get.get_subscribtion_price_by_title(title='LIGHT')
    is_have_enough_money = database_utils.Check\
        .check_user_have_enough_money(user_id=callback.message.chat.id, amount=amount)
    if is_have_enough_money:
        await buying_approve(message=callback.message, sub_type='LIGHT')
    else:
        await buying_failure(message=callback.message)


@router.callback_query(F.data == "buy_standard")
async def callback_buy_standard(callback: CallbackQuery) -> Coroutine:
    """отработка колбэка на покупку подписки типа standard

    Args:
        callback (CallbackQuery): колбэк с сообщения

    Returns:
        Coroutine: на выходе несколько корутин
    """
    amount = database_utils.Get.get_subscribtion_price_by_title(title='STANDARD')
    is_have_enough_money = database_utils.Check\
        .check_user_have_enough_money(user_id=callback.message.chat.id, amount=amount)
    if is_have_enough_money:
        await buying_approve(message=callback.message, sub_type='STANDARD')
    else:
        await buying_failure(message=callback.message)

@router.callback_query(F.data == "buy_premium")
async def callback_buy_premium(callback: CallbackQuery) -> Coroutine:
    """отработка колбэка на покупку подписки типа premium

    Args:
        callback (CallbackQuery): колбэк с сообщения

    Returns:
        Coroutine: на выходе несколько корутин
    """
    amount = database_utils.Get.get_subscribtion_price_by_title(title='PREMIUM')
    is_have_enough_money = database_utils.Check\
        .check_user_have_enough_money(user_id=callback.message.chat.id, amount=amount)
    if is_have_enough_money:
        await buying_approve(message=callback.message, sub_type='PREMIUM')
    else:
        await buying_failure(message=callback.message)


@router.callback_query(F.data.startswith('buying|'))
async def callback_buying_subcribtion(callback: CallbackQuery) -> Coroutine:
    """отработка колбэка под процесс покупки подписки

    Args:
        callback (CallbackQuery): колбэк с сообщения

    Returns:
        Coroutine: на выходе несколько корутин
    """
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
    amount = database_utils.Get.get_subscribtion_price_by_title(title={sub_title})
    database_utils.Update.update_user_balance_by_user_id(user_id=callback.message.chat.id, amount=(-1*amount))
    markup_inline = only_to_main.get()
    await callback.message.delete()
    invite = await bot.create_chat_invite_link(chat_id=-1001975523437, member_limit=1)
    await callback.message.answer('✅ Вы успешно приобрели подписку\n\n'\
                                  f'Ссылка для вступления 👇:\n\n {invite.invite_link}',
                                  reply_markup=markup_inline)