import asyncio

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Dispatcher, types
from sql_db import sql_add_profile, sql_read
from loader import dp
import random
from aiogram.utils.callback_data import CallbackData
from contextlib import suppress
from aiogram.utils.exceptions import (MessageToEditNotFound, MessageCantBeEdited, MessageCantBeDeleted, MessageToDeleteNotFound)

@dp.message_handler(commands=['profile'])
async def echo(message: types.Message):
    read = await sql_read()
    random_profile = random.choice(read)
    photo_item = random_profile[0]
    name_item = random_profile[1]
    age_item = random_profile[2]
    await message.answer_photo(photo_item, caption=f'{name_item} {age_item}')

vote_cb = CallbackData('vote', 'action')
def get_keyboard():
    return types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton('👍 ', callback_data=vote_cb.new(action='ups')),
        types.InlineKeyboardButton('👎 ', callback_data=vote_cb.new(action='down')),
        types.InlineKeyboardButton('ℹ️ Подробнее', callback_data=vote_cb.new(action='detail_profile')),
        types.InlineKeyboardButton('📧 Написать', callback_data=vote_cb.new(action='write_letter')),
        types.InlineKeyboardButton('🗑️ Жалоба', callback_data=vote_cb.new(action='spam_profile'))
    )


# async def get_profile():
#     read = await sql_read()
#     random_profile = random.choice(read)
#     photo_item = random_profile[0]
#     name_item = random_profile[1]
#     age_item = random_profile[2]
#     return photo_item, name_item, age_item





@dp.message_handler(commands='search')
async def cmd_start(message: types.Message):
    read = await sql_read()
    random_profile = random.choice(read)
    photo_item = random_profile[0]
    name_item = random_profile[1]
    age_item = random_profile[2]
    await message.answer_photo(photo_item, caption=f'{name_item} {age_item}', reply_markup=get_keyboard())

# @dp.callback_query_handler(vote_cb.filter(action='ups'))
async def vote_up_cb_handler(call: types.CallbackQuery, callback_data: dict):
    read = await sql_read()
    random_profile = random.choice(read)
    photo_item = random_profile[0]
    name_item = random_profile[1]
    age_item = random_profile[2]
    await call.message.answer_photo(photo_item, caption=f'{name_item} {age_item}', reply_markup=get_keyboard())
    await call.answer("Вы проголосовали за ❤️")
    await call.answer()
    await asyncio.sleep(1)
    await call.message.delete()

async def vote_down_cb_handler(call: types.CallbackQuery, callback_data: dict):
    read = await sql_read()
    random_profile = random.choice(read)
    photo_item = random_profile[0]
    name_item = random_profile[1]
    age_item = random_profile[2]
    await call.message.answer_photo(photo_item, caption=f'{name_item} {age_item}', reply_markup=get_keyboard())
    await call.answer("Вы проголосовали против")
    await call.answer()
    await asyncio.sleep(0.5)
    await call.message.delete()





async def vote_spam_cb_handler(call: types.CallbackQuery, callback_data: dict):
    await call.answer("Сообщение о спаме отавлено админу")
    await dp.bot.send_message(679511059, "Жалоба на профиль")












class FSMProfile(StatesGroup):
    photo = State()
    name = State()
    age = State()
    gender = State()
    hobby = State()
    chat_id = State()

#запрос у пользвателя на загрузку фото при команде Load
# @dp.message_handler(commands="Load", state=None)



#     await FSMProfile.next()


async def msg_load_photo(message: types.Message):
    await FSMProfile.photo.set()
    await message.answer("Загрузите фото")
    await message.answer(message.from_user.id)
#загрузка главных фото профиля и запрос имени
# @dp.message_handler(content_types="photo", state=FSMProfile.photo)
async def load_profile_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[-1].file_id
        data['chat_id'] = message.from_user.id
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
    dp.register_callback_query_handler(vote_down_cb_handler, vote_cb.filter(action='down'))
    dp.register_callback_query_handler(vote_spam_cb_handler, vote_cb.filter(action='spam_profile'))



