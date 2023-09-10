from pydantic_settings import BaseSettings
from pydantic import SecretStr

class BotConfig(BaseSettings):
    TOKEN: SecretStr
    USDT_WALLET: str
    
    class Config:
        env_file = 'config/.bot_config'
        env_file_encoding = 'utf-8'
        
class DatabaseConfig(BaseSettings):
    DATABASE_URL: SecretStr
    
    class Config:
        env_file = 'config/.database_config'
        env_file_encoding = 'utf-8'


bot_config = BotConfig()
database_config = DatabaseConfig()