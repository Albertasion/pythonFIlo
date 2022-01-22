from aiogram import types, Dispatcher
from loader import dp


# выбор языка
from FILO.keyboards.default.start_menu import hi_kb


@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    await message.answer("Приветсвую тебя на нашем сервисе", reply_markup=hi_kb)


def register_handlers_start(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=["start"])