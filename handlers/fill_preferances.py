import re
from itertools import islice

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from db import db_req
from db.db_req import pool
from handlers.states import Blank

fill_pref_router = Router()

@fill_pref_router.message(Blank.pref_gender)
async def set_pref_gender(message: Message, state: FSMContext):
    if message.content_type != 'text':
        await message.answer("You have typed not a text!")
        await state.set_state(Blank.pref_gender)
        return
    if message.text not in ['female', 'male']:
        await message.answer(f"There isn't such answer!")
        await state.set_state(Blank.pref_gender)
        return

    await state.update_data(pref_gender='f' if message.text == 'female' else 'm')
    print(f"{message.from_user.id}: add status 'pref_gender' - {'f' if message.text == 'female' else 'm'}")
    await state.set_state(Blank.pref_min_age)

    await message.answer("Enter MIN age to searching for:", reply_markup=ReplyKeyboardRemove())


@fill_pref_router.message(Blank.pref_min_age)
async def set_pref_min_age(message: Message, state: FSMContext):
    if message.content_type != 'text':
        await message.answer("You have typed not a text!")
        await state.set_state(Blank.pref_min_age)
        return
    if not re.fullmatch(r'\d+', message.text):
        await message.answer("Incorrect number!")
        await state.set_state(Blank.pref_min_age)
        return
    if int(message.text) < 10:
        await message.answer("Too little age!")
        await state.set_state(Blank.pref_min_age)
        return
    if int(message.text) > 80:
        await message.answer("Too big age!")
        await state.set_state(Blank.pref_min_age)
        return

    await state.update_data(pref_min_age=int(message.text))
    print(f"{message.from_user.id}: add status 'pref_min_age' - {int(message.text)}")
    await state.set_state(Blank.pref_max_age)

    await message.answer("Enter MAX age to searching for:", reply_markup=ReplyKeyboardRemove())


@fill_pref_router.message(Blank.pref_max_age)
async def set_pref_max_age(message: Message, state: FSMContext):
    if message.content_type != 'text':
        await message.answer("You have typed not a text!")
        await state.set_state(Blank.pref_max_age)
        return
    if not re.fullmatch(r'\d+', message.text):
        await message.answer("Incorrect number!")
        await state.set_state(Blank.pref_max_age)
        return
    if int(message.text) < 10:
        await message.answer("Too little age!")
        await state.set_state(Blank.pref_max_age)
        return
    if int(message.text) > 80:
        await message.answer("Too big age!")
        await state.set_state(Blank.pref_max_age)
        return

    await state.update_data(pref_max_age=int(message.text))
    print(f"{message.from_user.id}: add status 'pref_min_age' - {int(message.text)}")
    await state.set_state(Blank.pref_country)

    await message.answer("Enter country to searching for:", reply_markup=ReplyKeyboardRemove())

@fill_pref_router.message(Blank.pref_country)
async def set_pref_country(message: Message, state: FSMContext):
    if message.content_type != 'text':
        await message.answer("You have typed not a text!")
        await state.set_state(Blank.pref_country)
        return
    if re.search(r'\d', message.text):
        await message.answer("Country's name can't contain numbers!")
        await state.set_state(Blank.pref_country)
        return
    await state.update_data(pref_country=message.text.capitalize())
    print(f"{message.from_user.id}: add status 'pref_country' - {message.text}")
    await state.set_state(Blank.pref_city)

    await message.answer("Enter city to searching for:", reply_markup=ReplyKeyboardRemove())


@fill_pref_router.message(Blank.pref_city)
async def set_pref_city(message: Message, state: FSMContext):
    if message.content_type != 'text':
        await message.answer("You have typed not a text!")
        await state.set_state(Blank.pref_city)
        return
    if re.search(r'\d', message.text):
        await message.answer("City's name can't contain numbers!")
        await state.set_state(Blank.pref_city)
        return

    await state.update_data(pref_city=message.text.capitalize())
    print(f"{message.from_user.id}: add status 'pref_city' - {message.text}")

    keys_to_extract = ['pref_gender', 'pref_min_age', 'pref_max_age', 'pref_country', 'pref_city']
    user_data = await state.get_data()
    needed_user_data = {key: user_data[key] for key in keys_to_extract}

    await db_req.add_user_to_pref_tab(db_req.pool, message.from_user.id, **needed_user_data)
    print("pref DATA added")
