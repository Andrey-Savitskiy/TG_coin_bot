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
    if await is_password_correct(message.text):
        user = f"""
            tg_id = {message.from_user.id},
            name = '{message.from_user.first_name}',
            username = '{message.from_user.username}'
            """
        try:
            await commands.update(table='user', values=user, password=message.text)
            await message.answer(SETTINGS['commands']['start']['password_success'])
        except Exception as error:
            logger.exception(error)
            await message.answer(SETTINGS['error'])
        finally:
            await state.finish()
    else:
        await message.answer(SETTINGS['commands']['start']['password_error'])


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
    if await is_correct_time_format(message.text):
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
            await message.answer(SETTINGS['commands']['alert']['incorrect_date'])
    else:
        await message.answer(SETTINGS['commands']['alert']['incorrect_format'])


@dp.message_handler(commands=['info'], state=None)
async def cmd_alert(message: types.Message, state: FSMContext):
    if await is_user_auth(message.from_user.id):
        result = f'<b>Изменение цен монет за последние {MAX_DELTA_STATS} часов:</b>\n\n'
        try:
            for top_number in range(1, 11):
                coin = await commands.select_coin(top_number)
                coin_list = await commands.select_coins_by_name(name=coin[3], last_coin_id=coin[0])

                now = datetime.datetime.now()
                delta = datetime.timedelta(hours=MAX_DELTA_STATS)
                stat_list_filtered = list(filter(lambda x: x[3] == coin[3] and
                                                           now - datetime.datetime.strptime(x[4], '%Y-%m-%d %H:%M') <= delta,
                                                 coin_list))

                end_cost = float(coin[5])
                result_cost_list = list(map(lambda x: float(x[5]), stat_list_filtered))

                average_cost = sum(result_cost_list) / len(result_cost_list)

                if end_cost > average_cost:
                    result += f'{top_number}: <b>{coin[3]}</b> - да\n'
                else:
                    result += f'{top_number}: <b>{coin[3]}</b> - нет\n'

            await message.answer(result, parse_mode='HTML')
        except ZeroDivisionError:
            await message.answer('Данных пока нет. Повторите попытку позже.')

@dp.message_handler()
async def all_msg(message: types.Message):
    await message.answer('Такой команды нет!')
    await message.delete()
