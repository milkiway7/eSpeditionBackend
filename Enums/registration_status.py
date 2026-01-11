from enum import Enum

class RegistrationStatus(Enum):
    KRS_VERIFIED = "KRS_VERIFIED"
    ROLE_SELECTED = "ROLE_SELECTED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
