from fastapi import APIRouter, Depends
from dependencies import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from Routes.Registration.registration_dto import RegistrationStartDTO
from DataBase.Repositories.companies_repository import CompaniesRepository
from Exceptions.domain_exceptions import EntityAlreadyExistsError
from Services.krs_verification_service import verify_company_by_nip
from DataBase.Repositories.registration_repository import RegistrationsRepository
from .registration_mapper import RegistrationMapper

router = APIRouter()

@router.post("/registration/start")
async def start_registration(registration_dto: RegistrationStartDTO, session: AsyncSession = Depends(get_session)):
    # Check if company with NIP already exists in dB
    companies_repo = CompaniesRepository(session)
    existing_company = await companies_repo.get_by_company_for_registration(registration_dto.nip)
    if existing_company:
        raise EntityAlreadyExistsError("Company", "nip", registration_dto.nip)
    
    # Check if company with NIP exists in API Wykazu podatników VAT
    company_data = await verify_company_by_nip(registration_dto.nip)
    company_name = company_data.model_dump().get("company_name")

    #save in registrations table
    registration_db = RegistrationMapper.registration_start_dto_to_model(registration_dto, company_name)
    registrations_repo = RegistrationsRepository(session)  
    new_registration = await registrations_repo.start_registration(registration_db)

    return {"Registration started:": RegistrationMapper.db_model_to_dto(new_registration)}