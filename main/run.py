import asyncio
import os

from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from handlers.fill_blank import fill_blank_router
from handlers.fill_preferances import fill_pref_router
from db.db_req import on_startup

load_dotenv(dotenv_path='../config/.env')

bot = Bot(token=(os.getenv('TOKEN')), default=DefaultBotProperties(parse_mode='HTML'))
dp = Dispatcher(storage = MemoryStorage())


async def main():
    dp.include_router(fill_blank_router)
    dp.include_router(fill_pref_router)
    dp.startup.register(on_startup)

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")