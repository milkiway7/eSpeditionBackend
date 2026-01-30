from enum import Enum

class UserActivationStatus(Enum):
    PENDING = "PENDING"
    EXPIRED = "EXPIRED"
    USED = "USED"