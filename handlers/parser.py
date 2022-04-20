import asyncio
import datetime

import requests
from bs4 import BeautifulSoup as bs
import re

from loguru import logger

from db_api.sql import commands
from loader import TIMOUT_PARSER_COINS


URL = "https://bitinfocharts.com/ru/crypto-kurs/"


async def coin_parser():
    while True:
        try:
            result = {}

            request = requests.get(URL)
            result['time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

            if request.status_code == 200:
                soup = bs(request.text, "html.parser")
                coins = soup.find_all('tr', class_='ptr')

                result['top'] = 0
                for coin in coins:
                    result['top'] += 1
                    result['coin_id'] = coin['id']
                    result['coin_name'] = coin.select_one("td:nth-of-type(1)")['data-val']
                    result['cost'] = re.sub(r'[$ ]|,', '', coin.select_one("td:nth-of-type(2)").a.text)

                    await commands.insert(table='coins_data', columns=result.keys(), values=result.values())

                    if result['top'] == 10:
                        break

            else:
                logger.warning(f'Bad request: {request.status_code}')

            await asyncio.sleep(TIMOUT_PARSER_COINS)
        except Exception as error:
            logger.exception(error)
            continue
