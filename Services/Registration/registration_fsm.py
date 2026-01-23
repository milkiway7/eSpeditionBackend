from Enums.registration_status import RegistrationStatus

ALLOWED_TRANSITIONS = {
    RegistrationStatus.KRS_VERIFIED: {
        RegistrationStatus.DETAILS_COMPLETED
    },
    RegistrationStatus.DETAILS_COMPLETED: {
        RegistrationStatus.ROLE_SELECTED, # For CARRIER STATUS 
        RegistrationStatus.COMPLETED  # For SHIPPER STATUS 
    },
    RegistrationStatus.ROLE_SELECTED: {
        # CARRIER STATUS !!
        RegistrationStatus.COMPLETED,
        RegistrationStatus.FAILED
    },
    RegistrationStatus.COMPLETED: {
        RegistrationStatus.COMPLETED
    }
}