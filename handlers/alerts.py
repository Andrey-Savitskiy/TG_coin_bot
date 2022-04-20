import asyncio
import datetime

from loguru import logger
from db_api.sql import commands
from dispetcher import bot


async def check_alerts():
    while True:
        try:
            alerts_list = await commands.select_alerts()
            now = datetime.datetime.now()

            for alert in alerts_list:
                alert_time = datetime.datetime.strptime(alert[2], '%Y-%m-%d %H:%M')
                if alert_time <= now:
                    try:
                        await commands.remove(table='alert', id=alert[0])
                        await bot.send_message(chat_id=alert[1], text=alert[3])
                    except Exception as error:
                        logger.exception(error)
                        continue

            await asyncio.sleep(60)
        except Exception as error:
            logger.exception(error)
            continue
