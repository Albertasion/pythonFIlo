from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Dispatcher, types
from sql_db import sql_add_profile, sql_read
from loader import dp
import random
from aiogram.utils.callback_data import CallbackData

@dp.message_handler(commands=['profile'])
async def echo(message: types.Message):
    read = await sql_read()
    random_profile = random.choice(read)
    print(random_profile)
    photo_item = random_profile[0]
    name_item = random_profile[1]
    age_item = random_profile[2]
    await message.answer_photo(photo_item, caption=f'{name_item} {age_item}')

vote_cb = CallbackData('vote', 'action')
def get_keyboard():
    return types.InlineKeyboardMarkup().add(types.InlineKeyboardButton('Нравится', callback_data=vote_cb.new(action='ups')))

@dp.message_handler(commands='search')
async def cmd_start(message: types.Message):
    read = await sql_read()
    random_profile = random.choice(read)
    print(random_profile)
    photo_item = random_profile[0]
    name_item = random_profile[1]
    age_item = random_profile[2]
    await message.answer_photo(photo_item, caption=f'{name_item} {age_item}', reply_markup=get_keyboard())

# @dp.callback_query_handler(vote_cb.filter(action='ups'))
async def vote_up_cb_handler(call: types.CallbackQuery, callback_data: dict):
    read = await sql_read()
    random_profile = random.choice(read)
    print(random_profile)
    print(callback_data)
    photo_item = random_profile[0]
    name_item = random_profile[1]
    age_item = random_profile[2]
    await call.message.answer_photo(photo_item, caption=f'{name_item} {age_item}', reply_markup=get_keyboard())
#     # await call.answer_photo(photo_item, caption=f'{name_item} {age_item}', reply_markup=get_keyboard())
#     await call.message.answer(photo_item)
#     # await call.message.answer_sticker('CAACAgIAAxkBAAEDrK9h30SHP1bXS-Mp-S3F3SsiJh3i4wACUxMAAglroUll6QRkOIE6BCME')
#     # await call.answer("Вы проголосовали за ❤️")












class FSMProfile(StatesGroup):
    photo = State()
    name = State()
    age = State()
    gender = State()
    hobby = State()

#запрос у пользвателя на загрузку фото при команде Load
# @dp.message_handler(commands="Load", state=None)
async def msg_load_photo(message: types.Message):
    await FSMProfile.photo.set()
    await message.answer("Загрузите фото")
#загрузка главных фото профиля и запрос имени
# @dp.message_handler(content_types="photo", state=FSMProfile.photo)
async def load_profile_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[-1].file_id
        await FSMProfile.next()
        await message.answer("Введите ваше имя")
#захват имени польователя
async def load_name(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        data["name"] = message.text
        await FSMProfile.next()
        await message.answer("Введите ваш возвраст")
# захват ответа возраста и обработка возраста пользователя
async def load_age(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        data["age"] = message.text
        await message.answer("Выберите ваш пол")
        await FSMProfile.next()
#захват пола польователя и запрос хобби
async def load_gender(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        data["gender"] = message.text
        await FSMProfile.next()
        await message.answer("Введите ваши хобби")

# захват ответа хобби и обработка хобби пользователя
async def load_hobby(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["hobby"] = message.text
        await FSMProfile.next()
        await message.answer("Ваша анкета успешно загружена!")
        await message.answer(data)
        await message.answer(data.values())
        await sql_add_profile(state)
        await state.finish()

#собираем хендлеры регистрации нового пользователя
def register_handlers_profile_reg(dp : Dispatcher):
    dp.register_message_handler(msg_load_photo, commands="edit", state=None)
    dp.register_message_handler(load_profile_photo, content_types="photo", state=FSMProfile.photo)
    dp.register_message_handler(load_name, state=FSMProfile.name)
    dp.register_message_handler(load_age, state=FSMProfile.age)
    dp.register_message_handler(load_gender, state=FSMProfile.gender)
    dp.register_message_handler(load_hobby, state=FSMProfile.hobby)
    dp.register_callback_query_handler(vote_up_cb_handler, vote_cb.filter(action='ups'))


# from aiogram.utils.callback_data import CallbackData
# callback_numbers = CallbackData("fabnum", "action")
#
# def get_keyboard_fab():
#     buttons = [
#         types.InlineKeyboardButton(text="-1", callback_data=callback_numbers.new(action="decr")),
#         types.InlineKeyboardButton(text="-1", callback_data=callback_numbers.new(action="icr")),
#         types.InlineKeyboardButton(text="Подтвердить", callback_data=callback_numbers.new(action="finish"))
#     ]
#     keyboard = types.InlineKeyboardMarkup(row_width=2)
#     keyboard.add(*buttons)
#     return keyboard
#
# async def update_num_text_fab(message: types.Message, new_value:int):
#     with suppress(MessageNotModified):
#         await message.edit_text(f'Ukagite chislo:{new_value}', reply_markup=get_keyboard_fab())
#
# @dp.message_handler(commands="number_fab")
# async def cmd_numbers(message: types.Message):
#     user_data[message.from_user.id] = 0
#     await message.answer("Ukagite 0", reply_markup=get_keyboard_fab())
#
# @dp.callback_query_handler(callback_numbers.filter(action=["incr", "decr"]))
# async def callbacks_num_change_fab(call:types.CallbackQuery, callback_data:dict):
#     user_value = user_data.get(call.from_user.id, 0)
#     action=callback_data["action"]
#     if action=="incr":
#         user_data[call.from_user.id]=user_value+1
#         await update_num_text_fab(call.message, user_value+1)
#     elif action=="decr":
#         user_data[call.from_user.id]=user_value-1
#         await update_num_text_fab(call.message, user_value-1)
#     await call.answer()
#
# @dp.callback_query_handler(callback_numbers.filter(action=["finish"]))
# async def callbacks_num_finish_fab(call: types.CallbackQuery):
#     user_value = user_data.get(call.from_user.id, 0)
#     await call.message.edit_text(f"Итого: {user_value}")
#     await call.answer()