from Enums.registration_status import RegistrationStatus

ALLOWED_TRANSITIONS = {
    RegistrationStatus.KRS_VERIFIED: {
        RegistrationStatus.DETAILS_COMPLETED
    },
    RegistrationStatus.DETAILS_COMPLETED: {
        RegistrationStatus.ROLE_SELECTED
    },
    RegistrationStatus.ROLE_SELECTED: {
        RegistrationStatus.COMPLETED,
        RegistrationStatus.FAILED
    },
    RegistrationStatus.COMPLETED: {
        RegistrationStatus.COMPLETED
    }
}