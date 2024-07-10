from abc import ABC
from fastapi import HTTPException, status


class HTTPExceptionBase(HTTPException, ABC):
    """Base class for all exceptions"""

    status_code: status
    detail: str

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)
