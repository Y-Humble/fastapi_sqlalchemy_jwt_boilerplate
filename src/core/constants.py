from pathlib import Path


class Const:
    __slots__ = ()
    BASE_DIR: Path = Path(__file__).parent.parent
    ENVIRONS_DIR: Path = BASE_DIR / "environs"
    ENV_PATH: Path = BASE_DIR / "environs" / ".env"
    ENV_PROD_PATH: Path = ENVIRONS_DIR / ".env.prod"
    ENV_DEV_PATH: Path = ENVIRONS_DIR / ".env.dev"
    ENV_TEST_PATH: Path = ENVIRONS_DIR / ".env.test"
    CERTS_DIR: Path = ENVIRONS_DIR / "certs"
    PRIVATE_KEY_PATH: Path = CERTS_DIR / "private.pem"
    PUBLIC_KEY_PATH: Path = CERTS_DIR / "public.pem"
    NAMING_CONVENTION: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
