from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
)

# обычная клава
kb_choose_lang = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='🇺🇦 Ukrainian'),
            KeyboardButton(text='🇬🇧 English')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Enter data from keyboard"
)

kb_choose_gender  = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='female'),
            KeyboardButton(text='male')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Enter data from keyboard"
)

