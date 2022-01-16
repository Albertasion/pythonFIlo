from loader import dp
from aiogram import types


# выбор языка
@dp.message_handler(commands=['start'])
async def echo(message: types.Message):
    # await message.answer("Выбери язык", reply_markup=choice_language_keyb)


# колбек выбран русский язык
# @dp.callback_query_handler(text="ru_language_value")
# async def ru_choice_lang(call: types.CallbackQuery):
#     await call.message.answer("Вы выбрали русский язык")
#     await call.answer("Начнем заполнение данных")

