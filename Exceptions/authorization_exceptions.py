class AuthorizationException(Exception):
    def __init__(self, message: str = "Token has expired"):
        super().__init__(message)