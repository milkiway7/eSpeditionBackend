from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from Routes.User.user_dto import DtoLoginUser
from DataBase.Repositories.user_repository import UserRepository
from DataBase.Repositories.company_employees_repository import CompanyEmployeesRepository
from DataBase.Repositories.companies_repository import CompaniesRepository
from Services.password_encryption import verify_password
from Exceptions.domain_exceptions import UnauthorizedError
from datetime import datetime, timedelta, timezone
import jwt 
import os

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_SECONDS = 1800

class UserJWTData(BaseModel):
    sub: str
    email: str
    company_type: str
    user_role: str
    company_id: int
    iat: int

class AuthenticationService:
    async def authenticate(self, user_dto: DtoLoginUser, session: AsyncSession):
        try:
            repo = UserRepository(session)
            user = await repo.get_by_email(user_dto.email)

            if not verify_password(user_dto.password, user.password):
                raise UnauthorizedError("Invalid credentials")
            # To get company_id
            company_employees_repo = CompanyEmployeesRepository(session)
            company_employee = await company_employees_repo.get_by_user_id(user.id)
            # To get account_type
            companies_repo = CompaniesRepository(session)
            company = await companies_repo.get_by_id(company_employee.company_id)
            jwt_user = UserJWTData(
                sub=str(user.id),
                email=user.email,
                company_type=company.company_type,
                user_role=user.user_role,
                company_id=company_employee.company_id,
                iat=int(datetime.now(timezone.utc).timestamp())
            )
            jwt_token = self.generate_jwt(jwt_user)
            return {"access_token": jwt_token, "token_type": "bearer", "expires_in": ACCESS_TOKEN_EXPIRE_SECONDS}
        except Exception as e:
            raise UnauthorizedError(f"Authentication failed. {e}") from e
        
    def authenticate_after_registration(self, user: UserJWTData):
        jwt_token = self.generate_jwt(user)
        return {"access_token": jwt_token, "token_type": "bearer", "expires_in": ACCESS_TOKEN_EXPIRE_SECONDS}
    
    def generate_jwt(self, dto_user):
        to_encode = dto_user.model_dump()
        expire = datetime.now(timezone.utc) + timedelta(seconds=ACCESS_TOKEN_EXPIRE_SECONDS)
        to_encode.update({"exp": int(expire.timestamp())})
        token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return token