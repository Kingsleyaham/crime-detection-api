from enum import Enum

class MESSAGE(str, Enum):
    CREATED = 'Resource created successfully'
    UPDATED = 'Resource updated successfully'
    DELETED = 'Resource deleted successfully'
    USER_CREATED = 'User created successfully'

    # Error messages
    USER_NOT_FOUND = 'User not found'
    USER_ALREADY_EXISTS = 'User already exists'
    INVALID_CREDENTIALS = 'Invalid email or password'
    INVALID_TOKEN = 'Invalid access token'
