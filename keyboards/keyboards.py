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
    one_time_keyboard=True
)

kb_choose_gender = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='female'),
            KeyboardButton(text='male')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

kb_choose_pref_country = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='my country'),
            KeyboardButton(text='any')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

kb_choose_pref_city = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='my city'),
            KeyboardButton(text='any')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

kb_choose_publish_or_settings = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Publish and start searching')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
