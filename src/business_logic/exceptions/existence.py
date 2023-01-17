class AlreadyExistsError(Exception):
    def __init__(self, message: str):
        self.message = message


class DoesNotExistError(Exception):
    def __init__(self, message: str):
        self.message = message
