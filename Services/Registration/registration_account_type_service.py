from uuid import UUID
from Routes.Registration.registration_helpers import (
    check_registration_exists,
    validate_transition,
)
from DataBase.Repositories.registration_repository import RegistrationsRepository
from DataBase.TableModels.RegistrationsDbTableModel import RegistrationsDbTableModel
from Enums.registration_status import RegistrationStatus
from DataBase.Repositories.user_repository import UserRepository
from DataBase.Repositories.companies_repository import CompaniesRepository
from DataBase.Repositories.company_employees_repository import CompanyEmployeesRepository
from DataBase.TableModels.CompanyEmployeesDbTableModel import CompanyEmployeesDbTableModel
from Enums.company_type import CompanyType
from Enums.roles import Role
from Exceptions.registration_exceptions import RegistrationAccountTypeError
from Exceptions.domain_exceptions import ValidationError
from Services.authentication_service import AuthenticationService,UserJWTData
from Routes.Registration.registration_mapper import RegistrationMapper
from datetime import datetime, timezone

class RegistrationAccountTypeService:
    def __init__(self, session):
        self.session = session

    async def registration_account_type_orchestrator(
        self, registration_id: UUID, account_type: dict
    ):
        try: 
            async with self.session.begin():
                registration_repo = RegistrationsRepository(self.session)
                registration_to_update = await check_registration_exists(
                    registration_repo, registration_id
                )
                # check FSM
                validate_transition(
                    registration_to_update.registration_status,
                    RegistrationStatus.ROLE_SELECTED,
                )

                if account_type.get("account_type") == "SHIPPER":
                    jwt_token = await self.final_transaction(
                        registration_repo, registration_to_update, CompanyType.SHIPPER
                    )
                    return jwt_token
                elif account_type.get("account_type") == "CARRIER":
                    # Update status to ROLE_SELECTED in Registrations table
                    data_for_registration_update = {
                        "account_type": CompanyType.CARRIER,
                        "registration_status": RegistrationStatus.ROLE_SELECTED.value,
                    }
                    registration_updated = await registration_repo.final_registration_update(
                        registration_to_update,data_for_registration_update)
                    registration_dto = RegistrationMapper.db_model_to_dto(registration_updated)
                    return {"Role selected": "CARRIER", 
                            "Registration details": registration_dto}
                else:
                    raise ValidationError("Invalid account type provided")
        except Exception as e:
            raise RegistrationAccountTypeError(registration_to_update.id) 

    async def final_transaction(
        self,
        registration_repo: RegistrationsRepository,
        registration_to_update: RegistrationsDbTableModel,
        company_type: CompanyType,
    ):
        user_repository = UserRepository(self.session)
        new_user = await user_repository.create_from_registration(
            registration_to_update
        )
        
        company_repository = CompaniesRepository(self.session)
        new_company = await company_repository.create_from_registration(
            registration_to_update, company_type.value
        )
        # Wyślij inserty bez comita żeby dostać Id
        await self.session.flush()

        company_employee_repository = CompanyEmployeesRepository(self.session)
        await company_employee_repository.create_company_employee_link(
            CompanyEmployeesDbTableModel(
                company_id=new_company.id,
                user_id=new_user.id,
                role=Role.COMPANY_OWNER
            )
        )

        data_for_registration_update = {
            "account_type": company_type,
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
                account_type=company_type.value,
                role=Role.COMPANY_OWNER.value,
                company_id=new_company.id,
                iat=int(datetime.now(timezone.utc).timestamp())
            )
        )
        return user_jwt_data