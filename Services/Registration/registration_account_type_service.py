from uuid import UUID
from Services.Registration.registration_helpers import (check_registration_exists, validate_transition, 
                                                        final_transaction)
from DataBase.Repositories.registration_repository import RegistrationsRepository
from Enums.registration_status import RegistrationStatus
from Enums.company_type import CompanyType
from Enums.user_roles import UserRoles
from Exceptions.registration_exceptions import RegistrationAccountTypeError
from Exceptions.domain_exceptions import ValidationError
from Services.Registration.registration_mapper import RegistrationMapper

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
                    registration_id, registration_repo
                )
                # check FSM
                validate_transition(
                    registration_to_update.registration_status,
                    RegistrationStatus.ROLE_SELECTED,
                )

                if account_type.get("account_type") == "SHIPPER":
                    jwt_token = await final_transaction(
                        self.session, 
                        registration_repo, 
                        registration_to_update, 
                        CompanyType.SHIPPER, 
                        UserRoles.SHIPPER_ADMIN
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

    