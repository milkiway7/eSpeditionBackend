    
from Exceptions.registration_exceptions import RegistrationNotFoundError
from .registration_fsm import ALLOWED_TRANSITIONS
from Exceptions.domain_exceptions import ForbiddenError
from DataBase.Repositories.registration_repository import RegistrationsRepository
from DataBase.Repositories.user_repository import UserRepository
from DataBase.Repositories.companies_repository import CompaniesRepository
from DataBase.TableModels.RegistrationsDbTableModel import RegistrationsDbTableModel
from DataBase.Repositories.company_employees_repository import CompanyEmployeesRepository
from DataBase.TableModels.CompanyEmployeesDbTableModel import CompanyEmployeesDbTableModel
from Enums.company_type import CompanyType
from Enums.user_roles import UserRoles
from Enums.registration_status import RegistrationStatus
from Services.authentication_service import AuthenticationService, UserJWTData
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession

async def check_registration_exists(registration_id, repository: RegistrationsRepository):
    registration = await repository.get_by_registration_id(registration_id)
    if not registration:
        raise RegistrationNotFoundError(registration_id)
    return registration

def validate_transition(current_status, new_status):
    if new_status not in ALLOWED_TRANSITIONS.get(current_status, set()):
        raise ForbiddenError(f"Invalid registration transition from {current_status} to {new_status}")
    
async def final_transaction(
        session: AsyncSession,
        registration_repo: RegistrationsRepository,
        registration_to_update: RegistrationsDbTableModel,
        company_type: CompanyType,
        user_role: UserRoles
    ):
        user_repository = UserRepository(session)
        new_user = await user_repository.create_from_registration(
            registration_to_update, user_role.value
        )
        
        company_repository = CompaniesRepository(session)
        new_company = await company_repository.create_from_registration(
            registration_to_update, company_type.value
        )
        # Wyślij inserty bez comita żeby dostać Id
        await session.flush()

        company_employee_repository = CompanyEmployeesRepository(session)
        await company_employee_repository.create_company_employee_link(
            CompanyEmployeesDbTableModel(
                company_id=new_company.id,
                user_id=new_user.id
            )
        )

        data_for_registration_update = {
            "company_type": company_type,
            "registration_status": RegistrationStatus.COMPLETED.value,
        }
        await registration_repo.final_registration_update(
            registration_to_update, data_for_registration_update
        )

        auth_service = AuthenticationService()
        user_jwt_data = auth_service.authenticate_after_registration(
            UserJWTData(
                sub=str(new_user.id),
                email=new_user.email,
                user_role=new_user.user_role,
                company_type=company_type.value,
                company_id=new_company.id,
                iat=int(datetime.now(timezone.utc).timestamp())
            )
        )
        return user_jwt_data