from DataBase.database import Database
from Helpers.logger import get_logger
from DataBase.TableModels.UserDbTableModel import Base
import asyncio

INITIALIZATION_DB_MAX_RETRIES = 3
INITIALIZATION_DB_RETRY_DELAY = 7

async def initialize_database():
    for attempt in range(INITIALIZATION_DB_MAX_RETRIES):
        try:
            get_logger().info("Database initialization start")
            dB = Database()
            async with dB.engine.begin() as connection:
                await connection.run_sync(Base.metadata.create_all)
                get_logger().info("Database initialization success")
                return
        except Exception as e:
            if attempt < INITIALIZATION_DB_MAX_RETRIES:
                await asyncio.sleep(INITIALIZATION_DB_RETRY_DELAY)
            get_logger().error(f"Database initialization failed on attempt:{attempt + 1}. \n Error: {e}")

