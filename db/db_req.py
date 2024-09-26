import asyncpg, os

from asyncpg import Pool
from dotenv import load_dotenv
from datetime import date


load_dotenv()

pool = None


req_does_user_present_in_db = """SELECT * FROM user_private_info WHERE tg_id = $1"""

req_add_user_to_priv_tab = """
    INSERT INTO user_private_info(id, data, tg_id, lang_code, is_premium)
    VALUES ((SELECT COALESCE(MAX(id), 0) + 1 FROM user_private_info), $1, $2, $3, $4)
"""

req_add_user_to_public_tab = """
    INSERT INTO user_public_info(
        id, interface_lang, gender, name, age, country, city, description, photo
    )
    VALUES (
        (SELECT id FROM user_private_info WHERE tg_id = $1), 
        $2, $3, $4, $5, $6, $7, $8, $9
    )
"""

req_add_user_to_pref_tab = """
    INSERT INTO user_pref_info(
        id, gender, min_age, max_age, country, city
    )
    VALUES (
        (SELECT id FROM user_private_info WHERE tg_id = $1), 
        $2, $3, $4, $5, $6
    )
"""


async def on_startup():
    global pool
    pool = await create_pool()


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

async def add_user_to_public_tab(pool: Pool, tg_id: int, interface_lang: str, gender: str, name: str, age: int, country: str, city: str, description: str, photo: str) -> None:
    async with pool.acquire() as connection:
        await connection.execute(
            req_add_user_to_public_tab,
            tg_id, interface_lang, gender, name, age, country, city, description, photo
        )

async def add_user_to_pref_tab(pool: Pool, tg_id: int, pref_gender: str, pref_min_age: int, pref_max_age: int, pref_country: str, pref_city: str):
    async with pool.acquire() as connection:
        await connection.execute(
            req_add_user_to_pref_tab,
            tg_id, pref_gender, pref_min_age, pref_max_age, pref_country, pref_city)