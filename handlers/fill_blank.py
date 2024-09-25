from datetime import datetime

from db import db_req

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message


router = Router()
pool = None


async def on_startup():
    global pool
    pool = await db_req.create_pool()


@router.message(F.from_user.is_bot)
async def handler_bot_message(message: Message):
    return

@router.message(CommandStart())
async def bot_start(message: Message):
    if not await db_req.is_user_in_db(pool, message.from_user.id):
        print(f"There isn't user {message.from_user.id} in the private db")
        await db_req.add_user_to_priv_tab(
            pool = pool,
            data = datetime.now().date(),
            tg_id = message.from_user.id,
            lang_code = message.from_user.language_code,
            is_premium = message.from_user.is_premium if message.from_user.is_premium else False
        )
        print(f"User {message.from_user.id} has successfully added to priv_tab")

    print(f"User {message.from_user.id} exists in priv tab")


