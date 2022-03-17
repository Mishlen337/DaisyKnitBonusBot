from pydantic import BaseSettings
from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage


class Settings(BaseSettings):
    WEBHOOK_URL: str
    TELEGRAM_SECRET: str
    DB_PATH: str
    JOB_STORE_HOST: str
    JOB_STORE_PORT: str

    class Config:
        env_file = "./.env"


config = Settings()

storage = MemoryStorage()
bot = Bot(token=config.TELEGRAM_SECRET)
dp = Dispatcher(bot, storage=storage)
