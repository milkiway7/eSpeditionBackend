from enum import Enum

class Role(Enum):
    COMPANY_OWNER = "COMPANY_OWNER" # Może dać ADMIN ?
    EMPLOYEE = "EMPLOYEE"
    DRIVER = "DRIVER"
    DISPATCHER = "DISPATCHER" #Dyspozytor / logistyk
    