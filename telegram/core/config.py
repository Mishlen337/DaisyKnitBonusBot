from pydantic import BaseSettings
from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from typing import Optional


class Settings(BaseSettings):
    def __init__(self):
        super().__init__()
        self.aiogram_redis = {
            "host": self.REDIS_HOST,
            "port": self.REDIS_PORT,
            "password": None,
            "db": self.REDIS_DB
        }

    WEBHOOK_URL: str
    TELEGRAM_SECRET: str
    DB_PATH: str
    REDIS_HOST: Optional[str]
    REDIS_PORT: Optional[int]
    REDIS_DB: Optional[int]
    GOOGLE_AUTH_CREDS: Optional[str]
    GOOGLE_TABLE_ID: Optional[str]
    aiogram_redis: Optional[dict]
    TG_HOST: Optional[str]

    class Config:
        env_file = "./.env"


config = Settings()
# storage = MemoryStorage()
storage = RedisStorage2(**config.aiogram_redis)
bot = Bot(token=config.TELEGRAM_SECRET)
dp = Dispatcher(bot, storage=storage)
