from aiogram.fsm.state import StatesGroup, State

class Blank(StatesGroup):
    interface_lang = State()
    gender = State()
    name = State()
    age = State()
    country = State()
    city = State()
    description = State()
    photo = State()
    pref_gender = State()
    pref_min_age = State()
    pref_max_age = State()
    pref_country = State()
    pref_city = State()
    is_active = State()