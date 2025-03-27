class AppException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code


class UserAlreadyExists(AppException):
    def __init__(self):
        super().__init__("User already exists", 409)


class UserNotFoundException(AppException):
    def __init__(self):
        super().__init__("User not found", 404)