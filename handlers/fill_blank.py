from datetime import datetime
from typing import Callable

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from db import db_req

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message

from keyboards import keyboards


router = Router()
pool = None


async def on_startup():
    global pool
    pool = await db_req.create_pool()


@router.message(F.from_user.is_bot)
async def handler_bot_message(message: Message):
    return


class Blank(StatesGroup):
    interface_lang = State()
    gender = State()
    name = State()
    age = State()
    country = State()
    city = State()
    description = State()
    photo = State()


@router.message(CommandStart())
async def bot_start(message: Message, state: FSMContext):
    if not await db_req.is_user_in_db(pool, message.from_user.id):
        print(f"{message.from_user.id}: isn't in the private db")
        await db_req.add_user_to_priv_tab(
            pool = pool,
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


@router.message(Blank.interface_lang)
async def set_interface_lang(message: Message, state: FSMContext):
    if message.content_type != 'text':
        await message.answer(f"You have typed not a text!")
        await state.set_state(Blank.interface_lang)  # Возвращаем состояние
        return

    await state.update_data(interface_lang=message.text)
    print(f"{message.from_user.id}: add status 'interface_lang'")
    await state.set_state(Blank.gender)
    print(f"{message.from_user.id}: set status 'gender'")

    await message.answer("Choose your gender (male/female):")


@router.message(Blank.gender)
async def set_gender(message: Message, state: FSMContext):
    if message.content_type != 'text':
        await message.answer("You have typed not a text!")
        await state.set_state(Blank.gender)  # Возвращаем состояние
        return

    await state.update_data(gender=message.text)
    print(f"{message.from_user.id}: add status 'gender'")
    await state.set_state(Blank.name)
    print(f"{message.from_user.id}: set status 'name'")

    await message.answer("Enter your name:")


@router.message(Blank.name)
async def set_name(message: Message, state: FSMContext):
    if message.content_type != 'text':
        await message.answer("You have typed not a text!")
        await state.set_state(Blank.name)  # Возвращаем состояние
        return

    await state.update_data(name=message.text)
    print(f"{message.from_user.id}: add status 'name'")
    await state.set_state(Blank.age)
    print(f"{message.from_user.id}: set status 'age'")

    await message.answer("Enter your age:")


@router.message(Blank.age)
async def set_age(message: Message, state: FSMContext):
    if message.content_type != 'text':
        await message.answer("You have typed not a text!")
        await state.set_state(Blank.age)  # Возвращаем состояние
        return

    await state.update_data(age=message.text)
    print(f"{message.from_user.id}: add status 'age'")
    await state.set_state(Blank.country)
    print(f"{message.from_user.id}: set status 'country'")

    await message.answer("Enter your country:")


@router.message(Blank.country)
async def set_country(message: Message, state: FSMContext):
    if message.content_type != 'text':
        await message.answer("You have typed not a text!")
        await state.set_state(Blank.country)  # Возвращаем состояние
        return

    await state.update_data(country=message.text)
    print(f"{message.from_user.id}: add status 'country'")
    await state.set_state(Blank.city)
    print(f"{message.from_user.id}: set status 'city'")

    await message.answer("Enter your city:")


@router.message(Blank.city)
async def set_city(message: Message, state: FSMContext):
    if message.content_type != 'text':
        await message.answer("You have typed not a text!")
        await state.set_state(Blank.city)  # Возвращаем состояние
        return

    await state.update_data(city=message.text)
    print(f"{message.from_user.id}: add status 'city'")
    await state.set_state(Blank.description)
    print(f"{message.from_user.id}: set status 'description'")

    await message.answer("Enter a description about yourself:")


@router.message(Blank.description)
async def set_description(message: Message, state: FSMContext):
    if message.content_type != 'text':
        await message.answer("You have typed not a text!")
        await state.set_state(Blank.description)  # Возвращаем состояние
        return

    await state.update_data(description=message.text)
    print(f"{message.from_user.id}: add status 'description'")
    await state.set_state(Blank.photo)
    print(f"{message.from_user.id}: set status 'photo'")

    await message.answer("Please send your photo:")


@router.message(Blank.photo, F.photo)
async def set_photo(message: Message, state: FSMContext):
    if not message.photo:  # Проверка на наличие фото
        await message.answer("Please send your photo:")
        await state.set_state(Blank.photo)  # Возвращаем состояние
        return

    photo_id = message.photo[-1].file_id  # Получаем ID самой высокой четкости фото
    print(f"{message.from_user.id}: add status 'photo'")
    await state.update_data(photo=photo_id)

    await message.answer("Thank you! Your profile has been created.🎉")
    await message.answer(str(await state.get_data()))

    # Завершаем состояние
    await state.finish()
    print(f"{message.from_user.id}: State finished.")






