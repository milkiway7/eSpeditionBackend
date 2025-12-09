from pydantic import BaseModel, Field, EmailStr
from uuid import UUID

class UserModel(BaseModel):
    email: EmailStr
    password: str= Field(min_length=7)
    name: str= Field(min_length=2)
    surname: str=Field(min_length=2)
