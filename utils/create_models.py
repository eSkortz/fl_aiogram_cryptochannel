# * Импортируем все необходимые функции sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, BigInteger, DateTime, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base

# * импортируем конфиг бота и базы данных
from config.config_reader import database_config
from config.config_reader import bot_config

import datetime


engine = create_engine(database_config.DATABASE_URL.get_secret_value())
Base = declarative_base()


# * класс под таблицу users
class Users(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    telegram_id = Column(BigInteger, nullable=False)
    username = Column(String, unique=True, nullable=False)
    balance = Column(Float, default=0.0)
    registration_date = Column(DateTime, unique=False, default=datetime.datetime.now(), nullable=False)
    
# * класс под таблицу transactions
class Transactions(Base):
    __tablename__ = 'transactions'
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    transaction_hash = Column(String, unique=True, index=True, nullable=True)
    transaction_amount = Column(Float, nullable=True)
    from_user_id = Column(BigInteger, index=True, nullable=False)
    to_adress = Column(String, nullable=False, default=bot_config.USDT_WALLET)
    date_open = Column(DateTime, nullable=False, default=datetime.datetime.now())
    date_close = Column(DateTime, nullable=True)
    status = Column(Boolean, nullable=True, default=False)
    
# * класс под таблицу subscribtions 
class Subcriptions(Base):
    __tablename__ = 'subscriptions'
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(BigInteger)
    user_name = Column(String)
    date_start = Column(DateTime, nullable=False, default=datetime.datetime.now())
    date_over = Column(DateTime, nullable=False)
    sub_type = Column(String, nullable=False)
    
# * класс под таблицу tickets
class Tickets(Base):
    __tablename__ = 'tickets'
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(BigInteger)
    user_name = Column(String)
    question = Column(String, nullable=False)
    answer = Column(String, nullable=True)
    date_open = Column(DateTime, nullable=False, default=datetime.datetime.now())
    date_close = Column(DateTime, nullable=True)
    
# * класс под таблицу types_subscribtions
class Types_Subcribtions(Base):
    __tablename__ = 'types_subscribtions'
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    time = Column(Integer, nullable=False)
    

# * создаем все таблицы если они еще не существуют
def creating_models() -> None:
    Base.metadata.create_all(bind=engine)
