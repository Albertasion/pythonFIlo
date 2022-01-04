from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from loader import dp


@dp.callback_query_handler(text="hobby_value")
async def hobby_load(callback: types.CallbackQuery):
    await callback.message.answer("Privet")
    await callback.answer()

class FSMProfile(StatesGroup):
    photo = State()
    name = State()
    age = State()
    hobby = State()

#запрос у пользвателя на загрузку фото при команде Load
# @dp.message_handler(commands="Load", state=None)
async def msg_load_photo(message: types.Message):
    await FSMProfile.photo.set()
    await message.answer("Загрузите фото")
#загрузка главніх фото профиля
# @dp.message_handler(content_types="photo", state=FSMProfile.photo)
async def load_profile_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        print(message.photo)
        data['photo'] = message.photo[-1].file_id
        await FSMProfile.next()
        await message.answer("Ваше фото загружено")
        await message.answer_photo(data['photo'])
        await message.answer("Введите ваше имя")
#захват имени польователя
async def load_name(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        data["name"] = message.text
        await FSMProfile.next()
        await message.answer(f'Вас зовут {data["name"]}!')
        await message.answer("Введите ваш возвраст")

hobby_list = ["Автомобили", "Ароматерапия", "Астрономия", "Аэробика"]
#"Аэрография", "Бадминтон", "Батик", "Батут", "Бег", "Бильярд", "Блоггерство", "Бодиарт", "Боевые искусства", "Боулинг", "Велосипед", "Видеомонтаж", "Выращивание кристаллов", "Выращивание растений", "Вязание", "Гербари", "Головоломки", "Гольф", "Горные лыжи"]

keyboard_hobby_choice = InlineKeyboardMarkup(row_width=3)
for buttonshobby in hobby_list:
    hobbyButton = InlineKeyboardButton(text=buttonshobby, callback_data="hobby_value")
    keyboard_hobby_choice.row(hobbyButton)

# захват ответа возраста и обработка возраста пользователя
async def load_age(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        data["age"] = message.text
        await FSMProfile.next()
        await message.answer(f'Вас возвраст {data["age"]}!')
        await message.answer("Введите ваши хобби", reply_markup=keyboard_hobby_choice)


# захват ответа хобби и обработка хобби пользователя
async def load_hobby(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["hobby"] = message.text
        await FSMProfile.next()
        await message.answer(f'Ваше хобби {data["hobby"]}!')
        await message.answer("Ваша анкета успешно загружена!")
        await message.answer(f'Ваше имя {data["name"]}.Ваш возраст: {data["age"]}.Ваши хобби:{data["hobby"]}')

#собираем хендлеры регистрации нового пользователя
def register_handlers_profile_reg(dp : Dispatcher):
    dp.register_message_handler(msg_load_photo, commands="Load", state=None)
    dp.register_message_handler(load_profile_photo, content_types="photo", state=FSMProfile.photo)
    dp.register_message_handler(load_name, state=FSMProfile.name)
    dp.register_message_handler(load_age, state=FSMProfile.age)
    dp.register_message_handler(load_hobby, state=FSMProfile.hobby)