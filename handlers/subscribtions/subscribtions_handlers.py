from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile
from typing import Coroutine

# * импортируем ручки под бд
from utils import database_utils
# * импортируем разметку
from keyboards.subscribtions import trial, light, standard, premium

# * объявляем роутер
router = Router()


@router.callback_query(F.data == 'subscribtion_trial')
async def subscribtion_trial(callback: CallbackQuery) -> Coroutine:
    """отработка колбэка под раздел подписки trial

    Args:
        callback (CallbackQuery): колбэк с сообщения

    Returns:
        Coroutine: на выходе несколько корутин
    """
    markup_inline = trial.get()
    photo = FSInputFile('src/trial.jpg')
    days = database_utils.Get.get_subscribtion_days_by_title(title='TRIAL')
    await callback.message.delete()
    await callback.message.answer_photo(photo=photo, 
                                        caption=f'Это подписка 📙TRIAL, период ее действия {days} дней ' \
                                        '(можно активировать только один раз)', 
                                        reply_markup=markup_inline)
    

@router.callback_query(F.data == 'subscribtion_light')
async def subscribtion_light(callback: CallbackQuery) -> Coroutine:
    """отработка колбэка под раздел подписки light

    Args:
        callback (CallbackQuery): колбэк с сообщения

    Returns:
        Coroutine: на выходе несколько корутин
    """
    markup_inline = light.get()
    photo = FSInputFile('src/light.jpg')
    days = database_utils.Get.get_subscribtion_days_by_title(title='LIGHT')
    await callback.message.delete()
    await callback.message.answer_photo(photo=photo, 
                                        caption=f'Это подписка 📗LIGHT, период ее действия {days} дней ', 
                                        reply_markup=markup_inline)
    

@router.callback_query(F.data == 'subscribtion_standard')
async def subscribtion_standard(callback: CallbackQuery) -> Coroutine:
    """отработка колбэка под раздел подписки standard

    Args:
        callback (CallbackQuery): колбэк с сообщения

    Returns:
        Coroutine: на выходе несколько корутин
    """
    markup_inline = standard.get()
    photo = FSInputFile('src/standard.jpg')
    days = database_utils.Get.get_subscribtion_days_by_title(title='STANDARD')
    await callback.message.delete()
    await callback.message.answer_photo(photo=photo, 
                                        caption=f'Это подписка 📕STANDARD, период ее действия {days} дней ', 
                                        reply_markup=markup_inline)
    

@router.callback_query(F.data == 'subscribtion_premium')
async def subscribtion_premium(callback: CallbackQuery) -> Coroutine:
    """отработка колбэка под раздел подписки premium

    Args:
        callback (CallbackQuery): колбэк с сообщения

    Returns:
        Coroutine: на выходе несколько корутин
    """
    markup_inline = premium.get()
    photo = FSInputFile('src/premium.jpg')
    days = database_utils.Get.get_subscribtion_days_by_title(title='PREMIUM')
    await callback.message.delete()
    await callback.message.answer_photo(photo=photo, 
                                        caption=f'Это подписка 📘PREMIUM, период ее действия {days} дней ', 
                                        reply_markup=markup_inline)