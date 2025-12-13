from dotenv import load_dotenv
load_dotenv()

import uvicorn
from fastapi import FastAPI
from Api import location_api, user_api
from contextlib import asynccontextmanager
from DataBase.database_initialization import initialize_database
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    await initialize_database()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(location_api.router)
app.include_router(user_api.router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="localhost",
        port=8000,
        reload=True
    )
