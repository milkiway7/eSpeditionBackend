from fastapi import APIRouter, Depends
from dependencies import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from Routes.Registration.registration_dto import RegistrationStartDTO
from DataBase.Repositories.companies_repository import CompaniesRepository
from Exceptions.domain_exceptions import EntityAlreadyExistsError
from Services.krs_verification_service import verify_company_by_nip

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
    a = 1
    return {"message": "Registration started"}