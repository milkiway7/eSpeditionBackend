import uuid
from pydantic import BaseModel, EmailStr, Field

class RegistrationStartDTO(BaseModel):
    email: EmailStr
    password: str= Field(min_length=7)
    name: str= Field(min_length=2)
    surname: str=Field(min_length=2)    
    nip: str=Field(min_length=10, max_length=10)
    user_phone: str

class RegistrationReadDTO(BaseModel):
    registration_id: uuid.UUID
    company_name: str
    nip: str

class CompanyDetailsDTO(BaseModel):
    company_country: str
    company_city: str
    company_street: str
    company_building_number: str
    company_postal_code: str
    company_email: EmailStr
    company_phone: str

class AccountType(BaseModel):
    account_type: str