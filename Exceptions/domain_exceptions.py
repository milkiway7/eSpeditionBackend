class EntityNotFoundError(Exception):
    def __init__(self, entity: str, entity_id: int):
        self.entity = entity
        self.entity_id = entity_id
        super().__init__(f"{entity} with id={entity_id} not found")


class EntityAlreadyExistsError(Exception):
    def __init__(self, entity: str, field: str, value):
        self.entity = entity
        self.field = field
        self.value = value
        super().__init__(f"{entity} with {field}={value} already exists")


class ValidationError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class UnauthorizedError(Exception):
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(message)


class ForbiddenError(Exception):
    def __init__(self, message: str = "Forbidden"):
        super().__init__(message)
