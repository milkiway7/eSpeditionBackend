class KrsInactiveError(Exception):
    def __init__(self, nip: str):
        self.nip = nip
        super().__init__(f"Company with NIP={nip} is inactive in KRS")