from fastapi import APIRouter, Depends
from dependencies import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from Routes.Registration.registration_dto import RegistrationStartDTO, CompanyDetailsDTO
from DataBase.Repositories.companies_repository import CompaniesRepository
from Exceptions.domain_exceptions import EntityAlreadyExistsError
from Exceptions.registration_exceptions import RegistrationNotFoundError
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

@router.post("/registration/company-details/{registration_id}")
async def add_company_details(registration_id: str, company_details: CompanyDetailsDTO, session: AsyncSession = Depends(get_session)):
    #check if registration exists by registration_id
    registrations_repo = RegistrationsRepository(session)
    registration_exists = await registrations_repo.get_by_registration_id(registration_id)
    if not registration_exists:
        raise RegistrationNotFoundError(registration_id)
    #check FSM

    # Save company details to registration table