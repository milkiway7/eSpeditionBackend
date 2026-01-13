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
    company_country: str
    company_city: str
    company_street: str
    company_building_number: str
    company_postal_code: str
    company_email: EmailStr
    company_phone: str

class AccountType(BaseModel):
    account_type: str