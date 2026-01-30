from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class DtoLoginUser(BaseModel):
    email: EmailStr
    password: str= Field(min_length=7)

class DtoAddByAdmin(BaseModel):
    email: EmailStr
    user_role: str
    name: Optional[str] = Field(default=None, min_length=2)
    surname: Optional[str] = Field(default=None, min_length=2)
    phone_number: Optional[str] = Field(default=None, min_length=9)

class DtoActivateUser(BaseModel):
    activation_token: str
    password: str= Field(min_length=7)
    name: str= Field(min_length=2)
    surname: str=Field(min_length=2)
    phone_number: str = Field(min_length=9)

    
