#!/usr/bin/python
from aiogram import executor

from handlers.users.start import register_handlers_start
from utils.set_bot_commands import set_default_commands
from create_profile import register_handlers_profile_reg
from sql_db import sql_start
from loader import dp
from utils.notify_admins import on_startup_notify

async def on_startup(dispatcher):
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)
    # Уведомление админе о запуске бота
    await on_startup_notify(dispatcher)
    sql_start()
#запуск функции загрузки данніх нового пользователя
register_handlers_profile_reg(dp)
register_handlers_start(dp)
# Запуск бота.Start bot.
executor.start_polling(dp, skip_updates=True, on_startup=on_startup)