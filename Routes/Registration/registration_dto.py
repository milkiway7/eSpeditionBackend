import uuid
from pydantic import BaseModel, EmailStr

class RegistrationStartDTO(BaseModel):
    email: EmailStr
    password: str
    name: str
    surname: str
    nip: str
    user_phone: str

class RegistrationReadDTO(BaseModel):
    registration_id: uuid.UUID
    company_name: str
    nip: str