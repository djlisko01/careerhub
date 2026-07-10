from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn

ENV_FILE = Path(__file__).parent.parent / ".env"

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_FILE, env_file_encoding="utf-8")

    # Database
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    POSTGRES_PORT: int
    POSTGRES_DB: str

    # App
    log_level: str = "INFO"

    # Auth
    SECRET_KEY: str
    TOKEN_ALGO: str = "HS256"

    @property
    def postgres_url(self) -> str:
        url = PostgresDsn.build(
            scheme="postgresql",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )
        return str(url)


# Pyright doesn't know BaseSettings fills required fields from the env/.env file,
# so it flags this call as missing arguments: https://github.com/pydantic/pydantic-settings/issues/201
settings = Settings()  # type: ignore[call-arg]
