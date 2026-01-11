from Domain.Fsm.registration_fsm import ALLOWED_TRANSITIONS

def validate_transition(current_status, new_status):
    if new_status not in ALLOWED_TRANSITIONS.get(current_status, set()):
        raise ValueError(f"Invalid transition from {current_status} to {new_status}")