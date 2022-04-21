import asyncio
import logging

from aiogram.utils.executor import Executor
from loguru import logger

from handlers.alerts import check_alerts
from handlers.commands import *
from handlers.parser import coin_parser
from utils.log_settings import InterceptHandler


def main():
    logging.basicConfig(handlers=[InterceptHandler()], level='WARNING')
    try:
        executor = Executor(dp, skip_updates=True, loop=asyncio.gather(check_alerts(), coin_parser()))
        executor.start_polling()
    except Exception as error:
        logger.exception(error)


if __name__ == '__main__':
    main()
