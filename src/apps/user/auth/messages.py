class AuthResponseMessage:
    __slots__ = ()
    _KEY_MESSAGE: str = "message"
    LOGOUT: dict[str, str] = {_KEY_MESSAGE: "Logged out successfully"}
    ABORT: dict[str, str] = {_KEY_MESSAGE: "All sessions was aborted"}
