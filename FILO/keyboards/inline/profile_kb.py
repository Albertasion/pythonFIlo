from aiogram.utils.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

vote_cb = CallbackData('vote', 'action')
def keyboard_profile():
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton('❤️ ', callback_data=vote_cb.new(action='ups')),
        InlineKeyboardButton('👎 ', callback_data=vote_cb.new(action='down'))
    ).row(
        InlineKeyboardButton('ℹ️ Подробнее', callback_data=vote_cb.new(action='detail_profile')),
        InlineKeyboardButton('📧 Написать', callback_data=vote_cb.new(action='write_letter')),
        InlineKeyboardButton('🗑️ Жалоба', callback_data=vote_cb.new(action='spam_profile'))
    )


# Кнопка для отмены стейта
cancel_button = InlineKeyboardButton(text="Отмена", callback_data="cancel")
cancel_markup = InlineKeyboardMarkup(inline_keyboard=[[cancel_button]])
# Клавиатура для выбора пола
gender_callback = CallbackData("gender", "description", "value")

metabolism_gender_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Мужской",
                callback_data=gender_callback.new(description="мужчина", value="male"),
            ),
            InlineKeyboardButton(
                text="Женский",
                callback_data=gender_callback.new(
                    description="женщина", value="female"
                ),
            ),
        ],
        [cancel_button],
    ]
)