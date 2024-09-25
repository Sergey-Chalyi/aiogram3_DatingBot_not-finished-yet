import asyncpg, os

from asyncpg import Pool
from dotenv import load_dotenv
from datetime import date


load_dotenv()

req_does_user_present_in_db = """SELECT * FROM user_private_info WHERE tg_id = $1"""

req_add_user_to_priv_tab = """
    INSERT INTO user_private_info(id, data, tg_id, lang_code, is_premium)
    VALUES ((SELECT COALESCE(MAX(id), 0) + 1 FROM user_private_info), $1, $2, $3, $4)
"""


async def create_pool():
    return await asyncpg.create_pool(
        database=os.getenv('db_name'),
        host=os.getenv('host'),
        user=os.getenv('user'),
        password=os.getenv('password')
    )


async def is_user_in_db(pool: Pool, tg_id: int):
    async with pool.acquire() as connection:
        return await connection.fetchrow(req_does_user_present_in_db, tg_id)


async def add_user_to_priv_tab(pool: Pool, data: date, tg_id: int, lang_code: str, is_premium: bool) -> None:
    async with pool.acquire() as connection:
        await connection.execute(req_add_user_to_priv_tab, *(data, tg_id, lang_code, is_premium))

