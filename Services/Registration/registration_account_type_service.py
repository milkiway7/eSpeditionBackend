# Ten serwis:
# sprawdza FSM
# decyduje shipper vs carrier
# koordynuje inne serwisy
# zarządza transakcją
# To jest orchestrator, nie „helper”.
from uuid import UUID
from Routes.Registration.registration_helpers import check_registration_exists,validate_transition
from DataBase.Repositories.registration_repository import RegistrationsRepository
from Enums.registration_status import RegistrationStatus

class RegistrationAccountTypeService:
    def __init__(self, session):
        self.session = session

    async def registration_account_type_orchestrator(self, registration_id: UUID, account_type: dict):
        registration_repo = RegistrationsRepository(self.session)
        registration_to_update = await check_registration_exists(registration_repo, registration_id)
        #check FSM
        validate_transition(registration_to_update.registration_status, RegistrationStatus.ROLE_SELECTED)

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