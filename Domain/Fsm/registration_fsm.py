from Enums.registration_status import RegistrationStatus

ALLOWED_TRANSITIONS = {
    RegistrationStatus.KRS_VERIFIED: {
        RegistrationStatus.ROLE_SELECTED,
        RegistrationStatus.COMPLETED,
        RegistrationStatus.FAILED
    },
    RegistrationStatus.ROLE_SELECTED: {
        RegistrationStatus.COMPLETED,
        RegistrationStatus.FAILED
    },
    RegistrationStatus.COMPLETED: {
        RegistrationStatus.COMPLETED
    }
}