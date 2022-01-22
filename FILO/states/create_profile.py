from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMProfile(StatesGroup):
    photo = State()
    name = State()
    age = State()
    gender = State()
    hobby = State()
    chat_id = State()