from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

button_hi = KeyboardButton('Привет!')
button_byu = KeyboardButton('Пока!')

greet_kb = ReplyKeyboardMarkup(resize_keyboard=True)
hi_kb = greet_kb.add(button_hi, button_byu)