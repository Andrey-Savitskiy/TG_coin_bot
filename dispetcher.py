from aiogram import Dispatcher, Bot
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import loader
from loader import TOKEN

storage = MemoryStorage()

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, loop=loader.loop, storage=storage)
dp.middleware.setup(LoggingMiddleware())
