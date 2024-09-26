import re

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from db import db_req
from handlers.states import Blank
from keyboards import keyboards

search_router = Router()

@search_router.message(Blank.is_active)
async def set_activity(message: Message, state: FSMContext):
    if message.content_type != 'text':
        await message.answer("You have typed not a text!")
        await state.set_state(Blank.is_active)
        return
    if message.text not in ['Publish and start searching']:
        await message.answer("No such option!")
        await state.set_state(Blank.is_active)
        return

    if message.text == 'Publish and start searching':
        await db_req.set_activity(db_req.pool, message.from_user.id, True)
        print(f'{message.from_user.id}: activity DATA added')
