from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from loader import dp
from aiogram import Bot























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
        # await dp.bot.send_message(679511058, "Bot startoval")
#захват имени польователя
async def load_name(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        data["name"] = message.text
        await FSMProfile.next()
        # await message.answer(f'Вас зовут {data["name"]}!')
        await message.answer("Введите ваш возвраст")

keyboard_gender_choice = types.InlineKeyboardMarkup()
gendermaleButton = InlineKeyboardButton(text="Мужчина", callback_data="gender_male")
genderfemaleButton = InlineKeyboardButton(text="Женщина", callback_data="gender_female")
keyboard_gender_choice.row(gendermaleButton, genderfemaleButton)

#захват пола
async def select_gender(callback: types.CallbackQuery):
    await callback.message.answer("Genshina")
    await callback.answer()
    await load_gender()

# захват ответа возраста и обработка возраста пользователя
async def load_age(message: types.Message, state:FSMContext):
    await message.answer(message)
    async with state.proxy() as data:
        data["age"] = message.text
        await message.answer("Выберите ваш пол", reply_markup=keyboard_gender_choice)
        await FSMProfile.next()

#захват пола польователя и запрос хобби
async def load_gender(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        data["gender"] = message.text
        await FSMProfile.next()
        await message.answer(f'Ваш пол {data["gender"]}!')
        await message.answer("Введите ваши хобби")

# захват ответа хобби и обработка хобби пользователя
async def load_hobby(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["hobby"] = message.text
        await message.answer("Ваша анкета успешно загружена!")
        await message.answer(f'Ваше имя {data["name"]}.Ваш возраст: {data["age"]}.Ваши хобби:{data["hobby"]}, {data["gender"]}')
        await state.finish()



#собираем хендлеры регистрации нового пользователя
def register_handlers_profile_reg(dp : Dispatcher):
    dp.register_message_handler(msg_load_photo, commands="edit", state=None)
    dp.register_message_handler(load_profile_photo, content_types="photo", state=FSMProfile.photo)
    dp.register_message_handler(load_name, state=FSMProfile.name)
    dp.register_message_handler(load_age, state=FSMProfile.age)
    dp.register_message_handler(load_gender, state=FSMProfile.gender)
    dp.register_callback_query_handler(select_gender, text="gender_male", state=FSMProfile.gender)
    dp.register_message_handler(load_hobby, state=FSMProfile.hobby)