from pydantic import BaseModel


class CorsSettings(BaseModel):
    origins: list[str]
    headers: list[str]
    methods: list[str]
