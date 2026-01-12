from uuid import UUID
from fastapi import APIRouter, Depends
from Routes.Registration.validate_registration_transition import validate_transition
from dependencies import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from Routes.Registration.registration_dto import RegistrationStartDTO, CompanyDetailsDTO
from DataBase.Repositories.companies_repository import CompaniesRepository
from Exceptions.domain_exceptions import EntityAlreadyExistsError
from Exceptions.registration_exceptions import RegistrationNotFoundError
from Services.krs_verification_service import verify_company_by_nip
from DataBase.Repositories.registration_repository import RegistrationsRepository
from .registration_mapper import RegistrationMapper
from Enums.registration_status import RegistrationStatus

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
async def add_company_details(registration_id: UUID, data: CompanyDetailsDTO, session: AsyncSession = Depends(get_session)):
    #check if registration exists by registration_id
    registrations_repo = RegistrationsRepository(session)
    registration_to_update = await registrations_repo.get_by_registration_id(registration_id)
    if not registration_to_update:
        raise RegistrationNotFoundError(registration_id)
    #check FSM
    data_dict = data.model_dump(exclude_unset=True)

    validate_transition(registration_to_update.registration_status, RegistrationStatus.DETAILS_COMPLETED)
    
    # Save company details to registration table
    data_dict["registration_status"] = RegistrationStatus.DETAILS_COMPLETED
    updated_registration = await registrations_repo.update_company_details(registration_to_update, data_dict)

    return {"Company details added": RegistrationMapper.db_model_to_dto(updated_registration)}