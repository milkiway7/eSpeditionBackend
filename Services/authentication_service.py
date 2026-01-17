from pydantic import BaseModel
from Routes.User.user_dto import DtoLoginUser
from DataBase.Repositories.user_repository import UserRepository
from Services.password_encryption import verify_password
from Exceptions.domain_exceptions import UnauthorizedError
from datetime import datetime, timedelta
import jwt 
from Routes.User.user_mapper import UserMapper
import os

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_SECONDS = 1800

class UserJWTData(BaseModel):
    sub: int
    email: str
    account_type: str
    role: str
    exp: datetime | None

class AuthenticationService:
    async def authenticate(self, dto_user: DtoLoginUser, repo: UserRepository):
        user = await repo.get_by_email(dto_user.email)
        if not verify_password(dto_user.password, user.password):
            raise UnauthorizedError("Invalid credentials")
        dto_user = UserMapper.read_model_to_dto(user)
        jwt_token = self.generate_jwt(dto_user)
        return {"access_token": jwt_token, "token_type": "bearer", "expires_in": ACCESS_TOKEN_EXPIRE_SECONDS}

    def authenticate_after_registration(self, user: UserJWTData):
        jwt_token = self.generate_jwt(user)
        return {"access_token": jwt_token, "token_type": "bearer", "expires_in": ACCESS_TOKEN_EXPIRE_SECONDS}
    
    def generate_jwt(self, dto_user):
        to_encode = dto_user.model_dump()
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_SECONDS)
        to_encode.update({"exp": int(expire.timestamp())})
        token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return token