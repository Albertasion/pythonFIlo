from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


#клавиатура выбора языка
choice_language_keyb = InlineKeyboardMarkup()
rus_button = InlineKeyboardButton("Русский", callback_data="ru_language_value")
ua_button = InlineKeyboardButton("Українська", url="strument.com.ua")
en_button = InlineKeyboardButton("English", url="strument.com.ua")
choice_language_keyb.add(rus_button, ua_button, en_button)



