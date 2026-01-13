from Domain.Fsm.registration_fsm import ALLOWED_TRANSITIONS
from Exceptions.domain_exceptions import ForbiddenError
from Exceptions.registration_exceptions import RegistrationNotFoundError

def validate_transition(current_status, new_status):
    if new_status not in ALLOWED_TRANSITIONS.get(current_status, set()):
        raise ForbiddenError(f"Invalid registration transition from {current_status} to {new_status}")
    
async def check_registration_exists(registrations_repo, registration_id):
    registration = await registrations_repo.get_by_registration_id(registration_id)
    if not registration:
        raise RegistrationNotFoundError(registration_id)
    return registration