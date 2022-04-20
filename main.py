import asyncio
import logging

from aiogram.utils.executor import Executor
from loguru import logger

from handlers.alerts import check_alerts
from handlers.commands import *
from handlers.parser import coin_parser
from utils.log_settings import InterceptHandler


if __name__ == '__main__':
    logging.basicConfig(handlers=[InterceptHandler()], level='WARNING')
    try:
        loop = asyncio.get_event_loop()
        loop.create_task(check_alerts())
        loop.create_task(coin_parser())
        executor = Executor(dp, skip_updates=True)
        executor.start_polling()
    except Exception as error:
        logger.exception(error)
