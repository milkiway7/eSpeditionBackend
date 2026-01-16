from uuid import UUID

class KrsInactiveError(Exception):
    def __init__(self, nip: str):
        self.nip = nip
        super().__init__(f"Company with NIP={nip} is inactive in KRS")

class RegistrationNotFoundError(Exception):
    def __init__(self, registration_id: UUID):
        self.registration_id = registration_id
        super().__init__(f"Registration with registration_id={registration_id} not found")

class InvalidFinalTranzactionError(Exception):
    def __init__(self, registration_id: UUID):
        self.registration_id = registration_id
        super().__init__(f"Final transaction for registration_id={registration_id} failed")