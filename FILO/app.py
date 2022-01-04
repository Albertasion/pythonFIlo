#!/usr/bin/python
from aiogram import executor
from loader import dp
from start import *
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from create_profile import register_handlers_profile_reg
import sqlite3
sqlconnection = sqlite3.connect("data.db")
cur = sqlconnection.cursor()

#запуск функции загрузки данніх нового пользователя
register_handlers_profile_reg(dp)
# Запуск бота.Start bot.
executor.start_polling(dp, skip_updates=True)
