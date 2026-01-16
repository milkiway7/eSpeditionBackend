from uuid import UUID
from Routes.Registration.registration_helpers import (
    check_registration_exists,
    validate_transition,
)
from DataBase.Repositories.registration_repository import RegistrationsRepository
from DataBase.TableModels.RegistrationsDbTableModel import RegistrationsDbTableModel
from Enums.registration_status import RegistrationStatus
from .shipper_registration_flow_ervice import ShipperRegistrationService
from DataBase.Repositories.user_repository import UserRepository
from DataBase.TableModels.UserDbTableModel import UserDbTableModel
from DataBase.Repositories.companies_repository import CompaniesRepository
from DataBase.TableModels.CompaniesDbTableModel import CompaniesDbTableModel
from Enums.account_type import AccountType


class RegistrationAccountTypeService:
    def __init__(self, session):
        self.session = session

    async def registration_account_type_orchestrator(
        self, registration_id: UUID, account_type: dict
    ):
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
                await self.final_transaction(
                    registration_repo, registration_to_update, AccountType.SHIPPER
                )
            elif account_type.get("account_type") == "CARRIER":
                print("c")
            else:
                print("ERROR, account type doesn't exsist")
        # There will be 2 options SHIPPER and CARRIER
        # For shipper this is final step- so i neet to update status to COMPLETED and save account type to SHIPPER
        # Then create transatcion for shipper
        # BEGIN TRANSACTION
        # create company
        # create user
        # link user → company
        # mark registration COMPLETED
        # COMMIT
        # Retrun JWT TOKEN bcs he will be already logged in

        # For carrier update status to ROLE_SELECTED and save account type to CARRIER
        # return RegistrationReadDTO

    async def final_transaction(
        self,
        registration_repo: RegistrationsRepository,
        registration_to_update: RegistrationsDbTableModel,
        account_type: AccountType,
    ):
        user_repository = UserRepository(self.session)
        new_user = await user_repository.create_from_registration(
            registration_to_update, account_type.value
        )
        # Add item to company_users table
        company_repository = CompaniesRepository(self.session)
        new_company = await company_repository.create_from_registration(
            registration_to_update
        )
        
        data_for_registration_update = {
            "account_type": account_type,
            "registration_status": RegistrationStatus.COMPLETED.value,
        }

        await registration_repo.final_registration_update(
            registration_to_update, data_for_registration_update
        )
