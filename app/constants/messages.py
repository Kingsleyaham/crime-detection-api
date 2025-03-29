from enum import Enum

class MESSAGE(str, Enum):
    CREATED = 'Resource created successfully'
    UPDATED = 'Resource updated successfully'
    DELETED = 'Resource deleted successfully'
    USER_CREATED = 'User created successfully'

    # Error messages
    USER_NOT_FOUND = 'User not found'
    USER_ALREADY_EXISTS = 'User already exists'
    SHIFT_ALREADY_EXISTS = 'Shift already exists'
    SHIFT_NOT_FOUND = 'Shift not found'
    INVALID_CREDENTIALS = 'Invalid email or password'
    INVALID_TOKEN = 'Invalid access token'
    CANNOT_UPDATE_APPROVED_SHIFT = 'You cannot update approved shift'
    SHIFT_TIME_CONFLICT = 'Shift time conflict'
    INVALID_FILE_TYPE = 'Invalid file type. please upload a video.'
