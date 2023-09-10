import requests
import json

from config.config_reader import bot_config
from utils import database_utils

def check_transaction_by_hash(hash: str) -> tuple:
    response = requests.get(f'https://apilist.tronscanapi.com/api/transaction-info?hash={hash}')
    result = json.loads(response.text)
    
    try:
        status = result['contractRet']
        confirm_status = bool(result['confirmed'])
        adress = result['transfersAllList'][0]['to_address']
        amount = int(result['transfersAllList'][0]['amount_str'])/1000000
    except Exception:
        return False, 0.0
    
    valid_adress = bot_config.USDT_WALLET
    is_in_base = database_utils.Check.check_transactions_by_hash(hash=hash)
    
    # print(status, confirm_status, adress, is_in_base)
    
    if adress == valid_adress and status == 'SUCCESS' and confirm_status == True and is_in_base == False:
        return True, amount
    return False, amount
    
    