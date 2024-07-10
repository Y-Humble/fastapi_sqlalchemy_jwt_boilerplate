from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict

from core.config.auth import AuthSettings
from core.constants import Const
from core.config.database import DBSettings
from core.config.cors import CorsSettings
from core.config.run import RunSettings

type ModeT = Literal["DEV", "PROD", "TEST"]


class Settings(BaseSettings):
    """
    Application settings
        auth - algorithm, token_type_field, token_url, access_token_type,
        refresh_token_type, access_token_expire_minutes,
        refresh_token_expire_minutes
        run - host, port, app_title, log_level
        cors - origins, headers, methods
        db - driver, host, port, user, name, password,
            echo, echo_pool, pool_size, max_overflow
    """

    auth: AuthSettings
    db: DBSettings
    run: RunSettings
    cors: CorsSettings

    model_config = SettingsConfigDict(
        extra="allow",
        case_sensitive=False,
        env_nested_delimiter="__",
    )


class SettingsFactory(BaseSettings):
    """
    Returns a config instance depending on the MODE variable in the .env
    Mode - DEV, PROD, TEST
    """

    mode: ModeT
    model_config = SettingsConfigDict(
        env_file=Const.ENV_PATH, case_sensitive=False
    )

    def __call__(self) -> Settings:
        if self.mode == "PROD":
            return Settings(_env_file=Const.ENV_PROD_PATH)
        elif self.mode == "DEV":
            return Settings(_env_file=Const.ENV_DEV_PATH)
        elif self.mode == "TEST":
            return Settings(_env_file=Const.ENV_TEST_PATH)


settings: Settings = SettingsFactory()()
