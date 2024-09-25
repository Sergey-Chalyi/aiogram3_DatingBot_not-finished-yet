from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
)

# обычная клава
kb_choose_lang = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='🇺🇦 Ukrainian'),
            KeyboardButton(text='🇬🇧 English'),
            KeyboardButton(text='🇷🇺 Russian')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Enter data from keyboard"
)

