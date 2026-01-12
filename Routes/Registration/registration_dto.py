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

class CompanyDetailsDTO(BaseModel):
    country: str
    street: str
    building_number: str
    postal_code: str
    company_email: EmailStr
    company_phone: str