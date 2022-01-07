#!/usr/bin/python
from aiogram import executor
from start import *
from aiogram import types, Dispatcher
from create_profile import register_handlers_profile_reg

async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("edit", "✏    Редактировать анкету"),
            types.BotCommand("help", "👀    Просмотреть анкету"),
            types.BotCommand("search", "🔎    Начать поиск"),
            types.BotCommand("meet", "👍    Мои симпатии"),
            types.BotCommand("find", "☑️    Фильтр поиска"),
            types.BotCommand("balance", "Мой баланс"),
            types.BotCommand("present", "Мои подарки"),
            types.BotCommand("order", "Правила"),
            types.BotCommand("contact", "О нас")
        ]
    )

async def on_startup(dispatcher):
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)
    await dp.bot.send_message(679511059, "Bot startoval")


#запуск функции загрузки данніх нового пользователя
register_handlers_profile_reg(dp)
# Запуск бота.Start bot.
executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
