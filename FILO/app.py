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

async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("red", "Редактировать анкету"),
            types.BotCommand("help", "Просмотреть анкету"),
            types.BotCommand("search", "Начать поиск"),
            types.BotCommand("meet", "Мои знакомства"),
            types.BotCommand("find", "Фильтр поиска"),
            types.BotCommand("balance", "Мой баланс"),
            types.BotCommand("present", "Мои подарки"),
            types.BotCommand("order", "Правила"),
            types.BotCommand("contact", "О нас")
        ]
    )

async def on_startup(dispatcher):
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)


#запуск функции загрузки данніх нового пользователя
register_handlers_profile_reg(dp)
# Запуск бота.Start bot.
executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
