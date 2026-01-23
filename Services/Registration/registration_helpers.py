    
from Exceptions.registration_exceptions import RegistrationNotFoundError
from .registration_fsm import ALLOWED_TRANSITIONS
from Exceptions.domain_exceptions import ForbiddenError
from DataBase.Repositories.registration_repository import RegistrationsRepository

async def check_registration_exists(registration_id, repository: RegistrationsRepository):
    registration = await repository.get_by_registration_id(registration_id)
    if not registration:
        raise RegistrationNotFoundError(registration_id)
    return registration

def validate_transition(current_status, new_status):
    if new_status not in ALLOWED_TRANSITIONS.get(current_status, set()):
        raise ForbiddenError(f"Invalid registration transition from {current_status} to {new_status}")