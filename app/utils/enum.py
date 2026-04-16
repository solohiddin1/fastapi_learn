from enum import Enum

class ResultCodes(Enum):
    SUCCESS = 1
    FAIL = -1
    USER_ALREADY_EXISTS = -2
    USER_NOT_FOUND = -3
    USER_NOT_VERIFIED = -4
    INVALID_CREDENTIALS = -5
    POST_NOT_FOUND = -6
    PERMISSION_DENIED = -7


ResultMessages = {
    "SUCCESS": "Operation completed successfully.",
    "FAIL": "An error occurred during the operation.",
    "USER_ALREADY_EXISTS": "A user with this username already exists.",
    "USER_NOT_FOUND": "User not found.",
    "USER_NOT_VERIFIED": "User is not verified.",
    "INVALID_CREDENTIALS": "Invalid credentials.",
    "POST_NOT_FOUND": "Post not found.",
    "PERMISSION_DENIED": "Permission denied.",
}