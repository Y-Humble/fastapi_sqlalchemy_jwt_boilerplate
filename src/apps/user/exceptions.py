from core.exceptions import HTTPExceptionBase, status


class UserErrorMessages:
    __slots__ = ()
    INVALID_USER_401: str = "Invalid username or password"
    EMPTY_FORM_401: str = "Write username or email"
    DENIED_403: str = "Access is denied"
    FORBIDDEN_403: str = "Inactive user"
    USER_NOT_FOUND_404: str = "User not found"
    USERS_NOT_FOUND_404: str = "Users not found"
    USER_EXIST_409: str = "User already exists"


class InvalidCredentialsException(HTTPExceptionBase):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = UserErrorMessages.INVALID_USER_401


class EmptyCredentialsException(HTTPExceptionBase):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = UserErrorMessages.EMPTY_FORM_401


class AccessIsDeniedException(HTTPExceptionBase):
    status_code = status.HTTP_403_FORBIDDEN
    detail = UserErrorMessages.DENIED_403


class InactiveUserException(HTTPExceptionBase):
    status_code = status.HTTP_403_FORBIDDEN
    detail = UserErrorMessages.FORBIDDEN_403


class UserNotFoundException(HTTPExceptionBase):
    status_code = status.HTTP_404_NOT_FOUND
    detail = UserErrorMessages.USER_NOT_FOUND_404


class UsersNotFoundException(HTTPExceptionBase):
    status_code = status.HTTP_404_NOT_FOUND
    detail = UserErrorMessages.USERS_NOT_FOUND_404


class UserExistException(HTTPExceptionBase):
    status_code = status.HTTP_409_CONFLICT
    detail = UserErrorMessages.USER_EXIST_409
