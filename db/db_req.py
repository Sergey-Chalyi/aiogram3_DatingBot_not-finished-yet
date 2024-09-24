import asyncpg, os

from asyncpg import Pool
from dotenv import load_dotenv

load_dotenv()

req_does_user_present_in_db = """SELECT * FROM users_private_info WHERE tg_id = $1"""


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