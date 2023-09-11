from sqlalchemy import create_engine, select, update, values
from sqlalchemy.orm import sessionmaker

import datetime
from typing import Optional

# * импортируем конфиг бд
from config.config_reader import database_config
# * импортируем модели таблиц
from utils.create_models import Users, Transactions, Subcriptions, Tickets, Types_Subcribtions

# * объявляем движок и сессию
engine = create_engine(database_config.DATABASE_URL.get_secret_value())
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Check():
    """Условный класс, созданный для того, чтобы собрать внутри него
    все функции для проверки определенных значений по базе данных
    """

    def check_user_by_username(username: str) -> bool:
        """функция для проверки наличия пользователя в бд
        по юзернейму

        Args:
            username (str): юзернейм

        Returns:
            bool: наличие в бд
        """
        database = SessionLocal()
        query = select(Users).where(Users.username == username)
        result = database.execute(query).fetchone()
        database.close()
        if result:
            return True
        return False
    
    
    def check_user_by_telegram_id(telegram_id: int) -> bool:
        """Функция для проверки наличия пользователя в базе данных,
        используется для определения является ли пользователь новым
        пользователем

        Args:
            telegram_id (int): принимает на вход значение chat.id из сообщения пользователя

        Returns:
            bool: возвращает булево значения наличия пользователя в базе данных
        """
        database = SessionLocal()
        query = select(Users).where(Users.telegram_id == telegram_id)
        result = database.execute(query).fetchone()
        database.close()
        if result:
            return True
        return False


    def check_transactions_by_hash(hash: str) -> bool:
        """функция для проверки наличия транзакции в бд по хэшу

        Args:
            hash (str): хеш

        Returns:
            bool: наличие транзакции
        """
        database = SessionLocal()
        query = select(Transactions).where(Transactions.transaction_hash == hash)
        transaction = database.execute(query).fetchone()
        database.close()
        if transaction:
            return True
        return False
    

    def check_subcription_by_user_id(user_id: int) -> bool:
        """функция для проверки были ли подписки у пользователя по юзерайди

        Args:
            user_id (int): id пользователя

        Returns:
            bool: наличие подписок
        """
        database = SessionLocal()
        query = select(Subcriptions).where(Subcriptions.user_id == user_id)
        subscriptions = database.execute(query).fetchall()
        database.close()
        if subscriptions:
            return True
        return False


    def check_user_for_trial_subscribtion_by_user_id(user_id: int) -> bool:
        """проверка была ли у пользователя подписка триал

        Args:
            user_id (int): id пользователя

        Returns:
            bool: наличие триала
        """
        database = SessionLocal()
        query = select(Subcriptions).where((Subcriptions.user_id == user_id) & (Subcriptions.sub_type == 'TRIAL'))
        result = database.execute(query).fetchone()
        database.close()
        if result:
            return True
        return False

    
    def check_user_have_active_subcribtion(user_id: int) -> bool:
        """функция для проверки наличия активной подписки

        Args:
            user_id (int): id пользователя

        Returns:
            bool: наличие подписки
        """
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
        """функция для проверки достаточно ли у пользователя денег на аккаунте

        Args:
            user_id (int): id пользователя
            amount (float): сумма для проверки

        Returns:
            bool: наличие суммы на аккаунте
        """
        database = SessionLocal()
        query = select(Users.balance).where(Users.telegram_id == user_id)
        result = database.execute(query).fetchone()[0]
        database.close()
        if result > amount:
            return True
        return False


class Get():
    """Условный класс, созданнный для того, чтобы собрать внутри него
    все функции которые получают из базы данных определенные значение
    """

    def get_subscribtion_days_by_title(title: str) -> int:
        """функция для получения количества дней в подписке по ее названию

        Args:
            title (str): название подписки

        Returns:
            int: кол-во дней
        """
        database = SessionLocal()
        query = select(Types_Subcribtions.time).where(Types_Subcribtions.title == title)
        result = database.execute(query).fetchone()[0]
        database.close()
        return result
    
    
    def get_subscribtion_price_by_title(title: str) -> int:
        """функция для получения стоимости подписки по ее названию

        Args:
            title (str): название подписки

        Returns:
            int: стоимость подписки
        """
        database = SessionLocal()
        query = select(Types_Subcribtions.price).where(Types_Subcribtions.title == title)
        result = database.execute(query).fetchone()[0]
        database.close()
        return result
    
    
    def get_balance_by_telegram_id(telegram_id: int) -> float:
        """функция для получения баланса пользователя по id

        Args:
            telegram_id (int): id пользователя

        Returns:
            float: баланс пользователя
        """
        database = SessionLocal()
        query = select(Users.balance).where(Users.telegram_id == telegram_id)
        result = database.execute(query).fetchone()[0]
        database.close()
        return result
    
    
    def get_last_subscribtion_dateover_by_user_id(user_id: int) -> datetime:
        """функция для получения даты окончания последней подписки пользователя

        Args:
            user_id (int): id пользователя

        Returns:
            datetime: дата окончания
        """
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

    
    def get_last_subscribtion_id_by_user_id(user_id: int) -> int:
        """функция для получения id последней подписки пользователя по его id

        Args:
            user_id (int): id пользователя

        Returns:
            int: id подписки
        """
        database = SessionLocal()
        query = select(Subcriptions.id) \
                .where(Subcriptions.user_id == user_id) \
                .order_by(Subcriptions.date_over.desc()) \
                .limit(1)
        result = database.execute(query).fetchone()
        database.close()
        if result:
            return result[0]
        return False
    
    
    def get_five_tickets_by_user_id(user_id: int) -> tuple:
        """получение последних 5 тикетов пользователя

        Args:
            user_id (int): id пользователя

        Returns:
            tuple: последние 5 тикетов
        """
        database = SessionLocal()
        query = select(Tickets.question, Tickets.id)\
                .where(Tickets.user_id == user_id)\
                .order_by(Tickets.id.desc()).limit(5)
        result = database.execute(query).fetchall()
        database.close()
        return result
    
    
    def get_all_empty_tickets() -> tuple:
        """получение списка всех неотвеченных тикетов

        Returns:
            tuple: тикеты
        """
        database = SessionLocal()
        query = select(Tickets.question, Tickets.id)\
                .where(Tickets.answer == None)\
                .order_by(Tickets.id.desc())
        result = database.execute(query).fetchall()
        database.close()
        return result
    
    
    def get_all_users_telegramid() -> tuple:
        """получение списка всех id пользователей

        Returns:
            tuple: _description_
        """
        database = SessionLocal()
        query = select(Users.telegram_id)
        result = database.execute(query).fetchall()
        database.close()
        return result
    
    
    def get_ticket_by_id(ticket_id: int) -> tuple:
        """получение тикета по его id

        Args:
            ticket_id (int): id тикета

        Returns:
            tuple: тикет
        """
        database = SessionLocal()
        query = select(Tickets.question, Tickets.date_open, 
                    Tickets.answer, Tickets.date_close)\
                .where(Tickets.id == ticket_id).limit(1)
        result = database.execute(query).fetchone()
        database.close()
        return result
    
    
    def get_all_user_info_by_username(username: str) -> Optional[dict or int]:
        """получение информации по пользователю по его никнейму

        Args:
            username (str): никнейм пользователя

        Returns:
            Optional[dict or int]: 0 или информация о пользователе
        """
        database = SessionLocal()
        query = select(Users.telegram_id, Users.balance, Users.registration_date)\
                .where(Users.username == username).limit(1)
        result = database.execute(query).fetchone()
        if result:
            user_info = {
                'telegram_id' : result[0],
                'username' : f'@{username}',
                'balance' : f'{result[1]}$',
                'registration_date' : str(result[2])[:10],
            }
            user_info['is_activate_trial'] = Check\
                .check_user_for_trial_subscribtion_by_user_id(user_id=result[0])
            user_info['is_have_active_subscribe'] = Check\
                .check_user_have_active_subcribtion(user_id=result[0])
            return user_info
        else:
            return 0


class Create():
    """Условный класс, созданный для того, чтобы собрать внутри него
    все функции, которые используются для создания новых записей в 
    таблицах
    """

    def create_new_user(telegram_id: int, username: str) -> None:
        """создание нового пользователя в бд

        Args:
            telegram_id (int): id пользователя
            username (str): никнейм
        """
        database = SessionLocal()
        new_user = Users(telegram_id=telegram_id, username=username)
        database.add(new_user)
        database.commit()
        database.close()


    def create_new_transaction(hash: str, from_user_id: int, amount: float = None, status: bool = None, date = None) -> None:
        """создание новой транзакции в базе данных

        Args:
            hash (str): хэш транзакции
            from_user_id (int): id пользователя
            amount (float, optional): сумма транзакции (при наличии)
            status (bool, optional): статус транзакции (при наличии)
            date (_type_, optional): дата закрытия (при наличии)
        """
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
    


    def create_new_subscribtion(user_id: int, user_name: str, sub_type: str):
        """создание новой подписки в бд

        Args:
            user_id (int): id пользователя
            user_name (str): никнейм пользователя
            sub_type (str): тип подписки
        """
        database = SessionLocal()
        days_to_add = Get.get_subscribtion_days_by_title(title=sub_type)
        delta = datetime.timedelta(days=days_to_add)
        date_over = datetime.datetime.now() + delta
        new_subcribtion = Subcriptions(user_id=user_id, user_name=user_name, date_over=date_over, sub_type=sub_type)
        database.add(new_subcribtion)
        database.commit()
        database.close()
    

    def create_new_ticket(user_id: int, username: str, question: str) -> None:
        """создание нового тикета в бд

        Args:
            user_id (int): id пользователя
            username (str): никнейм
            question (str): содержание тикета
        """
        database = SessionLocal()
        new_ticket = Tickets(user_id=user_id, user_name=username, question=question)
        database.add(new_ticket)
        database.commit()
        database.close()
        
    
    def create_service_subscribe(username: str, days: int) -> None:
        """создание служебной подписки или добавление дней
        к текущей подписки (при ее наличии)

        Args:
            username (str): никнейм пользователя
            days (int): количество дней
        """
        database = SessionLocal()
        query = select(Users.telegram_id).where(Users.username == username).limit(1)
        user_id = database.execute(query).fetchone()[0]
        is_have_active_subcribe = Check.check_user_have_active_subcribtion(user_id=user_id)
        sub_id = Get.get_last_subscribtion_id_by_user_id(user_id=user_id)
        if sub_id and is_have_active_subcribe:
                Update.update_subscription_for_ndays(days=days, sub_id=sub_id)
        else:
            delta = datetime.timedelta(days=days)
            date_over = datetime.datetime.now() + delta
            new_subcribtion = Subcriptions(user_id=user_id, user_name=username, date_over=date_over, sub_type='SERVICE')
            database.add(new_subcribtion)
            database.commit()
            database.close()
            
class Update():
    """Условный класс, созданный для того, чтобы собрать внутри него
    все функции, которые используются для обновления полей в таблицах
    """

    def update_transaction_by_hash(hash: str, amount: float, date) -> None:
        """обновление транзакции по хэшу

        Args:
            hash (str): хэш транзакции
            amount (float): сумма для изменения
            date (_type_): дата закрытия
        """
        database = SessionLocal()
        query = update(Transactions).where(Transactions.transaction_hash == hash).values(transaction_amount=amount, status=True, date_close=date)
        database.execute(query)
        database.commit()
        database.close()
    
    
    def update_user_balance_by_user_id(user_id: int, amount: float) -> None:
        """обновление баланса пользователя

        Args:
            user_id (int): id пользователя
            amount (float): сумма для обновления
        """
        database = SessionLocal()
        query = select(Users.balance).where(Users.telegram_id == user_id)
        result = database.execute(query).fetchone()[0]
        new_balance = result + amount
        query = update(Users).where(Users.telegram_id == user_id).values(balance=new_balance)
        database.execute(query)
        database.commit()
        database.close()
        
        
    def update_subscription_for_ndays(days: int, sub_id) -> None:
        """прибавление дней к подписке по ее id в бд

        Args:
            days (int): кол-во дней
            sub_id (_type_): id подписки
        """
        days_to_add = datetime.timedelta(days=days)
        database = SessionLocal()
        query = select(Subcriptions.date_over).where(Subcriptions.id == sub_id).limit(1)
        date_over = database.execute(query).fetchone()[0]
        new_date = date_over + days_to_add
        query = update(Subcriptions).where(Subcriptions.id == sub_id).values(date_over=new_date)
        database.execute(query)
        database.commit()
        database.close()
        
    
    def update_answer_for_ticket_by_id(ticket_id: int, answer: str) -> None:
        """обновление ответа на тикет по его id в бд

        Args:
            ticket_id (int): id тикета
            answer (str): ответ на тикет
        """
        database = SessionLocal()
        date = datetime.datetime.now()
        query = update(Tickets).where(Tickets.id == ticket_id).values(answer=answer, date_close=date)
        database.execute(query)
        database.commit()
        database.close()