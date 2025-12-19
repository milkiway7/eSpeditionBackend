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
    created_at: datetime
    model_config = {"from_attributes": True}

