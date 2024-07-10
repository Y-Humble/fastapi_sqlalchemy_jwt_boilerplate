class UserResponseMessage:
    __slots__ = ()
    _KEY_MESSAGE = "message"
    INACTIVE_STATUS: dict[str, str] = {
        _KEY_MESSAGE: "User status is not active already"
    }
    DELETED_USER: dict[str, str] = {_KEY_MESSAGE: "User was deleted"}
    BANNED_USER: dict[str, str] = {_KEY_MESSAGE: "User was banned"}
