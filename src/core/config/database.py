from pydantic import BaseModel, SecretStr
from sqlalchemy import NullPool
from sqlalchemy.engine.url import URL


class DBSettings(BaseModel):
    driver: str
    host: str
    port: int
    user: str
    name: str
    password: SecretStr
    echo: bool
    echo_pool: bool
    pool_size: int
    max_overflow: int

    @property
    def url(self) -> URL:
        return URL.create(
            drivername=self.driver,
            username=self.user,
            password=self.password.get_secret_value(),
            host=self.host,
            port=self.port,
            database=self.name,
        )

    @property
    def engine_options(self):
        if self.name.startswith("test"):
            return {"poolclass": NullPool}
        return {"pool_size": self.pool_size, "max_overflow": self.max_overflow}
