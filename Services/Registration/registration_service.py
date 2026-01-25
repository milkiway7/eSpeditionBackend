from DataBase.Repositories.registration_repository import RegistrationsRepository
from DataBase.Repositories.companies_repository import CompaniesRepository
from Exceptions.domain_exceptions import EntityAlreadyExistsError
from Routes.Registration.registration_dto import (AccountType, RegistrationStartDTO, RegistrationReadDTO, CompanyDetailsDTO)
from Exceptions.domain_exceptions import EntityAlreadyExistsError
from Services.Registration.registration_helpers import check_registration_exists,validate_transition
from .krs_verification_service import verify_company_by_nip
from .registration_mapper import RegistrationMapper
from uuid import UUID
from Enums.registration_status import RegistrationStatus
from Enums.company_type import CompanyType
from .registration_account_type_service import RegistrationAccountTypeService
from sqlalchemy.ext.asyncio import AsyncSession

class RegistrationService:
    def __init__(self, repository:RegistrationsRepository):
        self.repository = repository

    async def start_registration(self,registration_dto: RegistrationStartDTO, companies_repo: CompaniesRepository) -> RegistrationReadDTO:
        # Check if company with NIP already exists in dB
        existing_company = await companies_repo.get_by_nip_for_registration(registration_dto.nip)
        if existing_company:
            raise EntityAlreadyExistsError("Company", "nip", registration_dto.nip)
        
        # Check if company with NIP exists in API Wykazu podatników VAT
        company_data = await verify_company_by_nip(registration_dto.nip)
        company_name = company_data.model_dump().get("company_name")

        #save in registrations table
        registration_db = RegistrationMapper.registration_start_dto_to_model(registration_dto, company_name)
        new_registration = await self.repository.start_registration(registration_db)

        return RegistrationMapper.db_model_to_dto(new_registration)
    

    async def add_company_details(self, registration_id: UUID, data: CompanyDetailsDTO) -> RegistrationReadDTO:
        registration_to_update = await check_registration_exists(registration_id, self.repository)
        #check FSM
        data_dict = data.model_dump(exclude_unset=True)
        validate_transition(registration_to_update.registration_status, RegistrationStatus.DETAILS_COMPLETED)
        # Save company details to registration table
        data_dict["registration_status"] = RegistrationStatus.DETAILS_COMPLETED
        updated_registration = await self.repository.update_company_details(registration_to_update, data_dict)

        return RegistrationMapper.db_model_to_dto(updated_registration)
    
    async def select_company_type(self, registration_id: UUID, account_type: AccountType, session = AsyncSession):
        # Save company details to registration table
        account_type_service = RegistrationAccountTypeService(session)
        response = await account_type_service.registration_account_type_orchestrator(registration_id,account_type.model_dump())
        return response
    
