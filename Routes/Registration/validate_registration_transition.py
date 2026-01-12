from Domain.Fsm.registration_fsm import ALLOWED_TRANSITIONS
from Exceptions.domain_exceptions import ForbiddenError

def validate_transition(current_status, new_status):
    if new_status not in ALLOWED_TRANSITIONS.get(current_status, set()):
        raise ForbiddenError(f"Invalid registration transition from {current_status} to {new_status}")