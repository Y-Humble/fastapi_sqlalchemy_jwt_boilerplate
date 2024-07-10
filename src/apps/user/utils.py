import bcrypt

from apps.user.auth.exceptions import InvalidTokenTypeException
from core.config import settings


def hash_password(password: str) -> bytes:
    salt: bytes = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def is_valid_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password)


def validate_token_type(payload: dict, expected_type: str) -> bool:
    token_type = payload.get(settings.auth.token_type_field)
    if token_type == expected_type:
        return True
    raise InvalidTokenTypeException(token_type, expected_type)
