from unittest.mock import call

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import message
from oauthlib.uri_validate import query

from config import *
from contextlib import suppress

from aiogram import types
from aiogram.utils.exceptions import (MessageToEditNotFound, MessageCantBeEdited, MessageCantBeDeleted,
    MessageToDeleteNotFound)


#инициализация бота
bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

import asyncio
import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.exceptions import MessageNotModified

logging.basicConfig(level=logging.INFO)

dp.middleware.setup(LoggingMiddleware())
























vote_cb = CallbackData('vote', 'action', 'amount')  # post:<action>:<amount>


def get_keyboard(amount):
    return types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton('👍 Нравится', callback_data=vote_cb.new(action='up', amount=amount)),
        types.InlineKeyboardButton('👎 Пропустить', callback_data=vote_cb.new(action='down', amount=amount)),
        types.InlineKeyboardButton('ℹ️ Подробнее', callback_data=vote_cb.new(action='detail_profile', amount=amount)),
        types.InlineKeyboardButton('📧 Написать', callback_data=vote_cb.new(action='write_letter', amount=amount)),
        types.InlineKeyboardButton('🗑️ Жалоба', callback_data=vote_cb.new(action='spam_profile', amount=amount))
    )
async def delete_message(message: types.Message, sleep_time: int = 0):
    await asyncio.sleep(sleep_time)
    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await message.delete()


@dp.message_handler(commands='search')
async def cmd_start(message: types.Message):
    await message.answer_photo('AgACAgIAAxkBAAIGBmHZjiqxpsaWLsVI0I8GNmmDMHJ7AAJEuTEb2p7ISgx2CrqzENccAQADAgADeAADIwQ', caption='<b>Petr</b>. 25 лет. <s>Киев.</s> <i>Украина</i>. ИТ специалист по безопасности. Интересы:<pre>Джаз</pre>', reply_markup=get_keyboard(0))



@dp.callback_query_handler(vote_cb.filter(action='up'))
async def vote_up_cb_handler(call: types.CallbackQuery, callback_data: dict):
    logging.info(callback_data)
    amount = int(callback_data['amount'])
    await call.message.answer(amount)
    await call.answer("Вы проголосовали за ❤️")
    await call.message.answer("Ждите ответ")
    amount+=1
    await bot.edit_message_text(f'You voted down! Now you have {amount} votes.',
                                query.from_user.id,
                                query.message.message_id,
                                reply_markup=get_keyboard(amount))








@dp.callback_query_handler(vote_cb.filter(action='down'))
async def vote_down_cb_handler(query: types.CallbackQuery, callback_data: dict):
    amount = int(callback_data['amount'])
    amount -= 1
    await bot.edit_message_text(f'You voted down! Now you have {amount} votes.',
                                query.from_user.id,
                                query.message.message_id,
                                reply_markup=get_keyboard(amount))
@dp.callback_query_handler(vote_cb.filter(action='detail_profile'))
async def vote_down_cb_handler(query: types.CallbackQuery, callback_data: dict):
    amount = int(callback_data['amount'])
    await bot.edit_message_text(f'You voted down! Now you have {amount} votes.',
                                query.from_user.id,
                                query.message.message_id,
                                reply_markup=get_keyboard(amount))



@dp.errors_handler(exception=MessageNotModified)  # for skipping this exception
async def message_not_modified_handler(update, error):
    return True
