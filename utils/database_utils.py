from sqlalchemy import create_engine, select, update, values

from sqlalchemy.orm import sessionmaker

from config_reader import database_config
from models import Users, Transactions, Subcriptions, Tickets, Types_Subcribtions

import datetime

engine = create_engine(database_config.DATABASE_URL.get_secret_value())

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def check_user_by_telegram_id(telegram_id: int) -> bool:
    database = SessionLocal()
    query = select(Users).where(Users.telegram_id == telegram_id)
    result = database.execute(query).fetchone()
    database.close()
    if result:
        return True
    return False


def check_transactions_by_hash(hash: str) -> bool:
    database = SessionLocal()
    query = select(Transactions).where(Transactions.transaction_hash == hash)
    transaction = database.execute(query).fetchone()
    database.close()
    if transaction:
        return True
    return False
    

def check_subcription_by_telegram_id(telegram_id: int) -> list:
    database = SessionLocal()
    query = select(Subcriptions).where(Subcriptions.user_id == telegram_id)
    subscriptions = database.execute(query).fetchall()
    database.close()
    return subscriptions


def create_new_user(telegram_id: int, username: str) -> None:
    database = SessionLocal()
    new_user = Users(telegram_id=telegram_id, username=username)
    database.add(new_user)
    database.commit()
    database.close()
    

def get_subscribtion_days_by_title(title: str) -> int:
    database = SessionLocal()
    query = select(Types_Subcribtions.time).where(Types_Subcribtions.title == title)
    result = database.execute(query).fetchone()[0]
    database.close()
    return result
    

def get_subscribtion_price_by_title(title: str) -> int:
    database = SessionLocal()
    query = select(Types_Subcribtions.price).where(Types_Subcribtions.title == title)
    result = database.execute(query).fetchone()[0]
    database.close()
    return result


def get_balance_by_telegram_id(telegram_id: int) -> float:
    database = SessionLocal()
    query = select(Users.balance).where(Users.telegram_id == telegram_id)
    result = database.execute(query).fetchone()[0]
    database.close()
    return result


def create_new_transaction(hash: str, from_user_id: int, amount: float = None, status: bool = None, date = None) -> None:
    database = SessionLocal()
    new_transaction = Transactions(transaction_hash = hash,
                                   transaction_amount = amount,
                                   from_user_id = from_user_id,
                                   date_close = date,
                                   status = status
                                   )
    database.add(new_transaction)
    database.commit()
    database.close()
    

def get_last_subscribtion_dateover_by_user_id(user_id: int) -> datetime:
    database = SessionLocal()
    query = select(Subcriptions.date_over) \
            .where(Subcriptions.user_id == user_id) \
            .order_by(Subcriptions.date_over.desc()) \
            .limit(1)
    result = database.execute(query).fetchone()
    database.close()
    if result:
        return result[0]
    return datetime.datetime.now()


def check_user_for_trial_subscribtion_by_user_id(user_id: int) -> bool:
    database = SessionLocal()
    query = select(Subcriptions).where((Subcriptions.user_id == user_id) & (Subcriptions.sub_type == 'TRIAL'))
    result = database.execute(query).fetchone()
    database.close()
    if result:
        return True
    return False


def check_user_have_active_subcribtion(user_id: int) -> bool:
    database = SessionLocal()
    query = select(Subcriptions.date_over) \
            .where(Subcriptions.user_id == user_id) \
            .order_by(Subcriptions.date_over.desc()) \
            .limit(1)
    result = database.execute(query).fetchone()
    database.close()
    if result:
        if result[0] > datetime.datetime.now():
            return True
    return False
    
    
def check_user_have_enough_money(user_id: int, amount: float) -> bool:
    database = SessionLocal()
    query = select(Users.balance).where(Users.telegram_id == user_id)
    result = database.execute(query).fetchone()[0]
    database.close()
    if result > amount:
        return True
    return False


def create_new_subscribtion(user_id: int, user_name: str, sub_type: str):
    database = SessionLocal()
    days_to_add = get_subscribtion_days_by_title(title=sub_type)
    delta = datetime.timedelta(days=days_to_add)
    date_over = datetime.datetime.now() + delta
    new_subcribtion = Subcriptions(user_id=user_id, user_name=user_name, date_over=date_over, sub_type=sub_type)
    database.add(new_subcribtion)
    database.commit()
    database.close()
    

def create_new_ticket(user_id: int, username: str, question: str) -> None:
    database = SessionLocal()
    new_ticket = Tickets(user_id=user_id, user_name=username, question=question)
    database.add(new_ticket)
    database.commit()
    database.close()
    

def get_five_tickets_by_user_id(user_id: int) -> tuple:
    database = SessionLocal()
    query = select(Tickets.question, Tickets.id)\
            .where(Tickets.user_id == user_id)\
            .order_by(Tickets.id.desc()).limit(5)
    result = database.execute(query).fetchall()
    database.close()
    return result


def get_ticket_by_id(ticket_id: int) -> tuple:
    database = SessionLocal()
    query = select(Tickets.question, Tickets.date_open, 
                   Tickets.answer, Tickets.date_close)\
            .where(Tickets.id == ticket_id).limit(1)
    result = database.execute(query).fetchone()
    database.close()
    return result


def update_transaction_by_hash(hash: str, amount: float, date) -> None:
    database = SessionLocal()
    query = update(Transactions).where(Transactions.transaction_hash == hash).values(transaction_amount=amount, status=True, date_close=date)
    database.execute(query)
    database.commit()
    database.close()
    
    
def update_user_balance_by_user_id(user_id: int, amount: float) -> None:
    database = SessionLocal()
    query = select(Users.balance).where(Users.telegram_id == user_id)
    result = database.execute(query).fetchone()[0]
    new_balance = result + amount
    print(new_balance)
    query = update(Users).where(Users.telegram_id == user_id).values(balance=new_balance)
    database.execute(query)
    database.commit()
    database.close()