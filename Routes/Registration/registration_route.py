from uuid import UUID
from fastapi import APIRouter, Depends
from Dependencies.get_session import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from Routes.Registration.registration_dto import RegistrationStartDTO, CompanyDetailsDTO, AccountType,TransportLicence
from DataBase.Repositories.registration_repository import RegistrationsRepository
from Services.Registration.registration_service import RegistrationService

router = APIRouter(prefix="/registration")

@router.post("/start")
async def start_registration(registration_dto: RegistrationStartDTO, session: AsyncSession = Depends(get_session)):
    registration_service = RegistrationService(RegistrationsRepository(session))
    registration_data = await registration_service.start_registration(registration_dto)
    return {"Registration started:": registration_data}

@router.post("/company-details/{registration_id}")
async def add_company_details(registration_id: UUID, data: CompanyDetailsDTO, session: AsyncSession = Depends(get_session)):
    registration_service = RegistrationService(RegistrationsRepository(session))
    registration_data = await registration_service.add_company_details(registration_id, data)
    return {"Company details added": registration_data}

@router.post("/select-company-type/{registration_id}")
async def select_company_type(registration_id: UUID, account_type: AccountType, session: AsyncSession = Depends(get_session)):
    registration_service = RegistrationService(RegistrationsRepository(session))
    registration_data = await registration_service.select_company_type(registration_id, account_type, session)
    return registration_data

@router.post("/transport-licence/{registration_id}")
async def add_transport_licence(registration_id: UUID, transport_licence: TransportLicence, session: AsyncSession = Depends(get_session)):
    # Placeholder for transport licence handling
    registration_service = RegistrationService(RegistrationsRepository(session))
    registration_data = await registration_service.transport_licence(registration_id, transport_licence, session)
    return registration_data