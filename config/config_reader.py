from pydantic_settings import BaseSettings
from pydantic import SecretStr

# * создаем класс для определения конфига токена и кошелька
class BotConfig(BaseSettings):
    TOKEN: SecretStr
    USDT_WALLET: str
    
    class Config:
        env_file = 'config/.bot_config'
        env_file_encoding = 'utf-8'
        
        
# * создаем класс для определения url базы данных
class DatabaseConfig(BaseSettings):
    DATABASE_URL: SecretStr
    
    class Config:
        env_file = 'config/.database_config'
        env_file_encoding = 'utf-8'

# * создаем объекты класса, которые будем испортировать в другие файлы
bot_config = BotConfig()
database_config = DatabaseConfig()