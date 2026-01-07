from dotenv import load_dotenv

load_dotenv()
import os
import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from DataBase.database_initialization import initialize_database
from fastapi.middleware.cors import CORSMiddleware
from Exceptions.exception_handlers import register_exception_handlers
from Routes.User import user_route
from Routes.Company import company_route

@asynccontextmanager
async def lifespan(app: FastAPI):
    await initialize_database()
    yield

app = FastAPI(lifespan=lifespan)

register_exception_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_route.router)
app.include_router(company_route.router)

if __name__ == "__main__":

    if os.getenv("ENVIRONMENT") == "DEV":
        host = os.getenv("HOST")
        port = int(os.getenv("PORT"))
    else:
        host = os.getenv("HOST")
        port = int(os.environ.get("PORT", 8000))

    uvicorn.run(
        "main:app",
        host= host,
        port= port,
        reload=True
    )
