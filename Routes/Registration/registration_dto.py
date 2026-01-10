from pydantic import BaseModel, EmailStr

class RegistrationStartDTO(BaseModel):
    email: EmailStr
    password: str
    name: str
    surname: str
    nip: str
    user_phone: str