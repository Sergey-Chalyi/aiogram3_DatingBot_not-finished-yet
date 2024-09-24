from db import db_req

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message


router = Router()
pool = None


async def on_startup():
    global pool
    pool = await db_req.create_pool()


@router.message(CommandStart())
async def bot_start(message: Message):
    if not await db_req.is_user_in_db(pool, message.from_user.id):
        print("+")
        pass
    else:
        pass

