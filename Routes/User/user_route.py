from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from DataBase.Repositories.user_repository import UserRepository
from dependencies import get_session
from Routes.User.user_dto import DtoCreateUser, DtoUpdateUser, DtoLoginUser
from Routes.User.user_mapper import UserMapper
from Services.authentication_service import AuthenticationService

router = APIRouter()

@router.get("/users/get_by_id/{user_id}")
async def get_user(user_id: int, session: AsyncSession = Depends(get_session)):
    repo = UserRepository(session)
    user = await repo.get_by_id(user_id)
    return {"User feched by id:": UserMapper.read_model_to_dto(user)}

@router.get("/users/get_by_email/{email}")
async def get_user_by_email(email: str, session: AsyncSession = Depends(get_session)):
    repo = UserRepository(session)
    user = await repo.get_by_email(email)
    return {"User feched by email:": UserMapper.read_model_to_dto(user)}

@router.post("/users/add")
async def add_user(dto_user: DtoCreateUser, session: AsyncSession = Depends(get_session)):
    db_user = UserMapper.create_dto_to_model(dto_user)
    repo = UserRepository(session)
    created_user = await repo.add_user(db_user)
    return {"User created:": UserMapper.read_model_to_dto(created_user)}

@router.put("/users/update/{user_id}")
async def update_user(user_id: int, dto_user: DtoUpdateUser, session: AsyncSession = Depends(get_session)):
    repo = UserRepository(session)
    updated_user = await repo.update_user(user_id, dto_user.model_dump(exclude_unset=True)) 
    return {"User updated:": UserMapper.read_model_to_dto(updated_user)}

    

@router.delete("/users/delete/{user_id}")
async def delete_user(user_id: int, session: AsyncSession = Depends(get_session)):
    repo = UserRepository(session)
    deleted_user = await repo.delete_user(user_id)
    return {"User deleted:": UserMapper.read_model_to_dto(deleted_user)}

    
@router.post("/users/authenticate")
async def login_user(dto_user: DtoLoginUser, session: AsyncSession = Depends(get_session)):
    repo = UserRepository(session)
    return await AuthenticationService().authenticate(dto_user, repo)

    
