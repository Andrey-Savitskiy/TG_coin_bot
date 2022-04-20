from db_api.sql import commands
import datetime


async def is_password_employed(password: str) -> bool:
    search_result = await commands.select_password(password)
    if search_result:
        return True
    else:
        return False


async def is_user_auth(tg_id: int) -> bool:
    search_result = await commands.select_user(tg_id)
    if search_result:
        return True
    else:
        return False


async def is_future_time(time: str) -> bool:
    user_time = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M')
    now = datetime.datetime.now()
    if user_time > now:
        return True
    else:
        return False
