from dotenv import load_dotenv
import os
import json
import asyncio

from loguru import logger

load_dotenv()

loop = asyncio.get_event_loop()

TOKEN = os.getenv('TOKEN')
try:
    TIMOUT_PARSER_COINS = int(os.getenv('TIMOUT_PARSER_COINS'))
    MAX_DELTA_STATS = int(os.getenv('MAX_DELTA_STATS'))
except ValueError as error:
    logger.exception(error)

with open('utils/text_settings.json', 'r', encoding='utf-8') as file:
    SETTINGS = json.loads(file.read())
