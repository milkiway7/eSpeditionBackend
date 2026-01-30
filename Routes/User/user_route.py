from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from DataBase.Repositories.user_repository import UserRepository
from Dependencies.get_session import get_session
from Dependencies.authorize_user import authorize_user
from Routes.User.user_dto import DtoLoginUser, DtoAddByAdmin, DtoActivateUser
from Services.authentication_service import AuthenticationService
from Services.User.user_service import UserService
import os
from DataBase.Repositories.user_activation_token_repository import ActivationUserRepository

router = APIRouter(prefix="/user")

@router.post("/login")
async def login_user(dto: DtoLoginUser, session: AsyncSession = Depends(get_session)):
    return await AuthenticationService().authenticate(dto, session)

@router.post("/admin-add", status_code=201)
async def admin_add_user(dto: DtoAddByAdmin,session: AsyncSession = Depends(get_session), user=Depends(authorize_user)):
    user_service = UserService(UserRepository(session))
    hash_token = await user_service.generate_activation_token(dto,user, session)
    return {"Activation url: ": f"{os.getenv("ESPEDITION_URL")}/user/activate?token={hash_token}"}

@router.put("/activate")
async def activate_user(dto: DtoActivateUser, session: AsyncSession = Depends(get_session)):
    user_service = UserService(UserRepository(session))
    jwt_token = await user_service.activate_user(dto, ActivationUserRepository(session), session)
    return jwt_token

    


    
