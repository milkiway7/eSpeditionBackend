from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from DataBase.Repositories.user_repository import UserRepository
from dependencies import get_session

router = APIRouter()

@router.get("/users/{user_id}")
async def get_user(user_id: int, session: AsyncSession = Depends(get_session)):
    repo = UserRepository(session)
    return await repo.get_by_id(user_id)