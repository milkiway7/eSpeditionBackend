from dotenv import load_dotenv
load_dotenv()
import uvicorn
from fastapi import FastAPI
from Api import location_api
from contextlib import asynccontextmanager 
from DataBase.database_initialization import initialize_database

@asynccontextmanager
async def lifespan(app: FastAPI):
    await initialize_database()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(location_api.router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )