from pydantic import BaseModel, Field
from typing import Optional

class DtoCreateCompany(BaseModel):
    nip: str= Field(min_length=10,max_length=10)
    vat_eu: Optional[str]= Field(default=None, max_length=20)
    country: str= Field(min_length=2, max_length=2)
    city: str= Field(min_length=2, max_length=100)
    postal_code: str= Field(min_length=2, max_length=20)
    street: str= Field(min_length=2, max_length=100)
    building_number: str= Field(min_length=1, max_length=10)
    website: Optional[str]= Field(default=None, max_length=100)
    phone_number: str= Field(min_length=8,max_length=15)
    company_name: str= Field(min_length=2, max_length=100)

class DtoReadCompany(BaseModel):
    id: int
    company_name: str
    country: str
    model_config = {"from_attributes": True}