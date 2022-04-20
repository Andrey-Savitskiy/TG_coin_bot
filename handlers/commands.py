import datetime
from functools import reduce

from aiogram import types
from aiogram.dispatcher import FSMContext
from loguru import logger

from dispetcher import dp
from handlers.form import FSMPasswordForm, FSMAlertForm
from loader import SETTINGS, MAX_DELTA_STATS
from utils.validators import *


@dp.message_handler(commands=['start'], state=None)
async def cmd_start(message: types.Message, state: FSMContext):
    if not await is_user_auth(message.from_user.id):
        await message.answer(SETTINGS['commands']['start']['start'])
        await FSMPasswordForm.password.set()


@dp.message_handler(state=FSMPasswordForm.password)
async def cmd_start_password(message: types.Message, state: FSMContext):
    if await is_password_employed(message.text):
        await message.answer(SETTINGS['commands']['start']['password_error'])
    else:
        user = {
            'tg_id': message.from_user.id,
            'name': message.from_user.first_name,
            'username': message.from_user.username,
            'password': message.text
        }
        try:
            await commands.insert(table='user', columns=user.keys(), values=user.values())
            await message.answer(SETTINGS['commands']['start']['password_success'])
        except Exception as error:
            logger.exception(error)
            await message.answer(SETTINGS['error'])
        finally:
            await state.finish()



@dp.message_handler(commands=['alert'], state=None)
async def cmd_alert(message: types.Message, state: FSMContext):
    if await is_user_auth(message.from_user.id):
        await message.answer(SETTINGS['commands']['alert']['start'])
        await FSMAlertForm.text.set()


@dp.message_handler(state=FSMAlertForm.text)
async def cmd_alert_time(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text

    await message.answer(SETTINGS['commands']['alert']['time'])
    await FSMAlertForm.next()


@dp.message_handler(state=FSMAlertForm.time)
async def cmd_alert_time(message: types.Message, state: FSMContext):
    if await is_future_time(message.text):
        async with state.proxy() as data:
            alert = {
                'text': data['text'],
                'tg_id': message.from_user.id,
                'time': message.text
            }

        try:
            await commands.insert(table='alert', columns=alert.keys(), values=alert.values())
            await message.answer(SETTINGS['commands']['alert']['success'])
        except Exception as error:
            logger.exception(error)
            await message.answer(SETTINGS['error'])
        finally:
            await state.finish()
    else:
        await message.answer(SETTINGS['commands']['alert']['incorrect'])


@dp.message_handler(commands=['info'], state=None)
async def cmd_alert(message: types.Message, state: FSMContext):
    if await is_user_auth(message.from_user.id):
        result = f'<b>Изменение цен монет за последние {MAX_DELTA_STATS} часов:</b>\n\n'
        for top_number in range(1, 11):
            stat_list = await commands.select_coin(top_number)

            coins = {}
            for line in stat_list:
                if line[3] in coins.keys():
                    coins[line[3]] += 1
                else:
                    coins[line[3]] = 1

            max_coin = 0
            max_coin_name = ''
            for key, value in coins.items():
                if value > max_coin:
                    max_coin = value
                    max_coin_name = key

            now = datetime.datetime.now()
            delta = datetime.timedelta(hours=MAX_DELTA_STATS)
            stat_list_filtered = list(filter(lambda x: x[3] == max_coin_name and
                                                       now - datetime.datetime.strptime(x[4], '%Y-%m-%d %H:%M') <= delta,
                                             stat_list))
            stat_list_sorted_id = sorted(stat_list_filtered, key=lambda x: x[0])

            end_cost = float(stat_list_sorted_id[-1][5])
            result_cost_list = list(map(lambda x: float(x[5]), stat_list_sorted_id[:-1]))
            average_cost = sum(result_cost_list) / len(result_cost_list)

            if end_cost < average_cost:
                result += f'<b>{top_number}</b>: {max_coin_name} ⏬\n'
            elif end_cost > average_cost:
                result += f'<b>{top_number}</b>: {max_coin_name} ⏫\n'
            else:
                result += f'<b>{top_number}</b>: {max_coin_name} ↔️\n'

        await message.answer(result, parse_mode='HTML')


@dp.message_handler()
async def all_msg(message: types.Message):
    await message.answer('Такой команды нет!')
    await message.delete()
