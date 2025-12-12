from fastapi import Depends
from DataBase.database import Database

db_instance = Database()

async def get_session():
    async with db_instance.session() as session:
        yield session
