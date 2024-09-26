from datetime import datetime
import re

from aiogram.fsm.context import FSMContext
from handlers.states import Blank

from db import db_req

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards import keyboards

fill_blank_router = Router()


@fill_blank_router.message(F.from_user.is_bot)
async def handler_bot_message(message: Message):
    return


@fill_blank_router.message(Blank.interface_lang)
async def set_interface_lang(message: Message, state: FSMContext):
    if message.content_type != 'text':
        await message.answer(f"You have typed not a text!")
        await state.set_state(Blank.interface_lang)
        return
    if message.text not in ['🇺🇦 Ukrainian', '🇬🇧 English']:
        await message.answer(f"There isn't such answer!")
        await state.set_state(Blank.interface_lang)
        return

    await state.update_data(interface_lang='ua' if message.text == '🇺🇦 Ukrainian' else 'eng')
    print(f"{message.from_user.id}: add status 'interface_lang' - {'ua' if message.text == '🇺🇦 Ukrainian' else 'eng'}")
    await state.set_state(Blank.gender)

    await message.answer(
        "Choose your gender (male/female):",
        reply_markup=keyboards.kb_choose_gender
    )


@fill_blank_router.message(Blank.gender)
async def set_gender(message: Message, state: FSMContext):
    if message.content_type != 'text':
        await message.answer("You have typed not a text!")
        await state.set_state(Blank.gender)
        return
    if message.text not in ['female', 'male']:
        await message.answer(f"There isn't such answer!")
        await state.set_state(Blank.gender)
        return

    await state.update_data(gender='f' if message.text == 'female' else 'm')
    print(f"{message.from_user.id}: add status 'gender' - {'f' if message.text == 'female' else 'm'}")
    await state.set_state(Blank.name)

    await message.answer("Enter your name:", reply_markup=ReplyKeyboardRemove())


@fill_blank_router.message(Blank.name)
async def set_name(message: Message, state: FSMContext):
    if message.content_type != 'text':
        await message.answer("You have typed not a text!")
        await state.set_state(Blank.name)
        return
    if not re.fullmatch(r'[A-Za-zА-Яа-яЁё]+', message.text):
        await message.answer("The name can`t contain spaces or numbers!")
        await state.set_state(Blank.name)
        return

    await state.update_data(name=message.text.capitalize())
    print(f"{message.from_user.id}: add status 'name' - {message.text.capitalize()}")
    await state.set_state(Blank.age)

    await message.answer("Enter your age:", reply_markup=ReplyKeyboardRemove())


@fill_blank_router.message(Blank.age)
async def set_age(message: Message, state: FSMContext):
    if message.content_type != 'text':
        await message.answer("You have typed not a text!")
        await state.set_state(Blank.age)
        return
    if not re.fullmatch(r'\d+', message.text):
        await message.answer("Incorrect number!")
        await state.set_state(Blank.age)
        return
    if int(message.text) < 10:
        await message.answer("Too little age!")
        await state.set_state(Blank.age)
        return
    if int(message.text) > 80:
        await message.answer("Too big age!")
        await state.set_state(Blank.age)
        return

    await state.update_data(age=int(message.text))
    print(f"{message.from_user.id}: add status 'age' - {int(message.text)}")
    await state.set_state(Blank.country)

    await message.answer("Enter your country:", reply_markup=ReplyKeyboardRemove())


@fill_blank_router.message(Blank.country)
async def set_country(message: Message, state: FSMContext):
    if message.content_type != 'text':
        await message.answer("You have typed not a text!")
        await state.set_state(Blank.country)
        return
    if re.search(r'\d', message.text):
        await message.answer("Country's name can't contain numbers!")
        await state.set_state(Blank.country)
        return

    await state.update_data(country=message.text.capitalize())
    print(f"{message.from_user.id}: add status 'country' - {message.text.capitalize()}")
    await state.set_state(Blank.city)

    await message.answer("Enter your city:", reply_markup=ReplyKeyboardRemove())


@fill_blank_router.message(Blank.city)
async def set_city(message: Message, state: FSMContext):
    if message.content_type != 'text':
        await message.answer("You have typed not a text!")
        await state.set_state(Blank.city)
        return
    if re.search(r'\d', message.text):
        await message.answer("City's name can't contain numbers!")
        await state.set_state(Blank.city)
        return

    await state.update_data(city=message.text.capitalize())
    print(f"{message.from_user.id}: add status 'city' - {message.text.capitalize()}")
    await state.set_state(Blank.description)

    await message.answer("Enter a description about yourself:", reply_markup=ReplyKeyboardRemove())


@fill_blank_router.message(Blank.description)
async def set_description(message: Message, state: FSMContext):
    if message.content_type != 'text':
        await message.answer("You have typed not a text!")
        await state.set_state(Blank.description)
        return
    if len(message.text) < 20:
        await message.answer("Your description is too short!")
        await state.set_state(Blank.description)
        return
    if len(message.text) > 200:
        await message.answer("Your description is too long!")
        await state.set_state(Blank.description)
        return

    await state.update_data(description=message.text)
    print(f"{message.from_user.id}: add status 'description' - {message.text}")
    await state.set_state(Blank.photo)

    await message.answer("Please send your photo:", reply_markup=ReplyKeyboardRemove())


@fill_blank_router.message(Blank.photo)
async def set_photo(message: Message, state: FSMContext):
    if message.content_type != 'photo':
        await message.answer("You have typed not a photo!")
        await state.set_state(Blank.photo)
        return

    print(f"{message.from_user.id}: add status 'photo' = {message.photo[-1].file_id}")
    await state.update_data(photo=message.photo[-1].file_id)

    await message.answer("Your profile has been created🎉")

    # save data to db
    user_data = await state.get_data()
    await db_req.add_user_to_public_tab(db_req.pool, message.from_user.id, **(user_data))
    print("public DATA added")

    await message.answer_photo(
        photo=user_data.get('photo'),
        caption=f"<b>{user_data.get('name')}, {user_data.get('age')}, {user_data.get('city')}</b>\n{user_data.get('description')}",
        parse_mode='html'
    )

    await message.answer("Okey, let's fill out your search preferences!", reply_markup=keyboards.kb_choose_gender)
    await state.set_state(Blank.pref_gender)


@fill_blank_router.message(CommandStart())
async def bot_start(message: Message, state: FSMContext):
    if not await db_req.is_user_in_db(db_req.pool, message.from_user.id):
        print(f"{message.from_user.id}: isn't in the private db")
        await db_req.add_user_to_priv_tab(
            pool = db_req.pool,
            data = datetime.now().date(),
            tg_id = message.from_user.id,
            lang_code = message.from_user.language_code,
            is_premium = message.from_user.is_premium if message.from_user.is_premium else False
        )
        print(f"{message.from_user.id}: has successfully added to priv_tab")

    print(f"{message.from_user.id}: exists in priv tab")

    await message.answer(
        "<b>Hello👋</b>\nThis bot is to help you with dating💕\nLet's make your blank!",
        parse_mode='html'
    )
    await message.answer(
        "Choose your language🌎:",
        reply_markup=keyboards.kb_choose_lang
    )

    await state.set_state(Blank.interface_lang)
    print(f"{message.from_user.id}: set status 'interface_lang'")




