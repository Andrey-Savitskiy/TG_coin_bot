from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMPasswordForm(StatesGroup):
    password = State()


class FSMAlertForm(StatesGroup):
    text = State()
    time = State()
