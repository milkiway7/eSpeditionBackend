from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

class DtoCreateUser(BaseModel):
    email: EmailStr
    password: str= Field(min_length=7)
    name: str= Field(min_length=2)
    surname: str=Field(min_length=2)

class DtoReadUser(BaseModel):
    id: int
    email: str
    name: str
    surname: str
    model_config = {"from_attributes": True}

class DtoUpdateUser(BaseModel):
    name: Optional[str]= Field(default=None, min_length=2)
    surname: Optional[str]=Field(default=None, min_length=2)
    password: Optional[str]= Field(default=None, min_length=7)
    email: Optional[EmailStr]= None

class DtoLoginUser(BaseModel):
    email: EmailStr
    password: str= Field(min_length=7)
