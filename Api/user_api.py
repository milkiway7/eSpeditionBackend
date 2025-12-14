from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from DataBase.Repositories.user_repository import UserRepository
from dependencies import get_session
from Api.Dto.dto_user import DtoCreateUser
from Helpers.mapper import UserMapper

router = APIRouter()

@router.get("/users/{user_id}")
async def get_user(user_id: int, session: AsyncSession = Depends(get_session)):
    repo = UserRepository(session)
    return await repo.get_by_id(user_id)

@router.post("/users/add")
async def add_user(dto_user: DtoCreateUser, session: AsyncSession = Depends(get_session)):
    # fetch user with specific email to check if exsists
    db_user = UserMapper.create_dto_to_model(dto_user)
    repo = UserRepository(session)
    return await repo.add(db_user)

@router.put("users/update")
async def update_user():
    pass

@router.delete("users/delete/{user_id}")
async def delete_user(user_id: int):
    pass

    
