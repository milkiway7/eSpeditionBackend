from uuid import UUID
from fastapi import APIRouter, Depends
from Dependencies.get_session import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from Routes.Registration.registration_dto import RegistrationStartDTO, CompanyDetailsDTO, AccountType
from DataBase.Repositories.companies_repository import CompaniesRepository
from DataBase.Repositories.registration_repository import RegistrationsRepository
from Services.Registration.registration_service import RegistrationService

router = APIRouter()

@router.post("/registration/start")
async def start_registration(registration_dto: RegistrationStartDTO, session: AsyncSession = Depends(get_session)):
    registration_service = RegistrationService(RegistrationsRepository(session))
    registration_data = await registration_service.start_registration(registration_dto, CompaniesRepository(session))
    return {"Registration started:": registration_data}

@router.post("/registration/company-details/{registration_id}")
async def add_company_details(registration_id: UUID, data: CompanyDetailsDTO, session: AsyncSession = Depends(get_session)):
    registration_service = RegistrationService(RegistrationsRepository(session))
    registration_data = await registration_service.add_company_details(registration_id, data)
    return {"Company details added": registration_data}

@router.post("/registration/select-company-type/{registration_id}")
async def select_company_type(registration_id: UUID, account_type: AccountType, session: AsyncSession = Depends(get_session)):
    registration_service = RegistrationService(RegistrationsRepository(session))
    registration_data = await registration_service.select_company_type(registration_id, account_type, session)
    return registration_data

@router.post("/registration/transport-licence/{registration_id}")
async def add_transport_licence(registration_id: UUID, licence_number: str, session: AsyncSession = Depends(get_session)):
    # Placeholder for transport licence handling
    return {"message": "Transport licence handling not implemented yet"}