from Api.UsersApi.dto_user import DtoLoginUser
from DataBase.Repositories.user_repository import UserRepository
from Api.UsersApi.password_encryption import verify_password
from Exceptions.domain_exceptions import UnauthorizedError
from datetime import datetime, timedelta
import jwt 
from Api.UsersApi.user_mapper import UserMapper
import os
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class AuthenticationService:
    async def authenticate(self, dto_user: DtoLoginUser, repo: UserRepository):
        user = await repo.get_by_email(dto_user.email)
        if not verify_password(dto_user.password, user.password):
            raise UnauthorizedError("Invalid credentials")
        dto_user = UserMapper.read_model_to_dto(user)
        jwt_token = self.generate_jwt(dto_user)
        return {"access_token": jwt_token, "token_type": "bearer", "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES, "user": dto_user}
    
    def generate_jwt(self, dto_user):
        to_encode = dto_user.model_dump()
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": int(expire.timestamp())})
        token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return token




