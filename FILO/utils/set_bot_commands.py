from aiogram import types
# меню
async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("edit", "✏    Редактировать анкету"),
            types.BotCommand("profile", "👀    Просмотреть анкету"),
            types.BotCommand("search", "🔎    Начать поиск"),
            types.BotCommand("meet", "👍    Мои симпатии"),
            types.BotCommand("find", "☑️    Фильтр поиска"),
            types.BotCommand("balance","💰    Мой баланс"),
            types.BotCommand("present", "🎁    Мои подарки"),
            types.BotCommand("order", "📜    Правила")
        ]
    )