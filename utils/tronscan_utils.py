import requests
import json

# * импортируем конфиг бота
from config.config_reader import bot_config
# * импортируем ручки для бд
from utils import database_utils

def check_transaction_by_hash(hash: str) -> tuple:
    """функция для проверки статуса транзакции через tronscan.org

    Args:
        hash (str): trxid транзацкии

    Returns:
        tuple: значение статуса транзакции и сумма
    """
    
    # * делаем запрос и получаем ответ в формате json, извлекаем из него текст
    response = requests.get(f'https://apilist.tronscanapi.com/api/transaction-info?hash={hash}')
    result = json.loads(response.text)
    
    # * пробуем найти все нужные поля в раскодированном json
    try:
        status = result['contractRet']
        confirm_status = bool(result['confirmed'])
        adress = result['transfersAllList'][0]['to_address']
        amount = int(result['transfersAllList'][0]['amount_str'])/1000000
    except Exception:
        return False, 0.0
    
    # * берем значение адреса кошелька из конфига и bool значение наличия такой транзакции в бд
    valid_adress = bot_config.USDT_WALLET
    is_in_base = database_utils.Check.check_transactions_by_hash(hash=hash)
    
    # * проверяем полученные значения и возвращаем результат
    if adress == valid_adress and status == 'SUCCESS' and confirm_status == True and is_in_base == False:
        return True, amount
    return False, amount
    
    