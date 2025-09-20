from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR.parent / ".env"


class Settings(BaseSettings):
    DATABASE_URL: str

    APP_NAME: str = "Your Beauty"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"

    model_config = SettingsConfigDict(
        env_file=ENV_PATH,
        env_file_encoding = "utf-8"
    )

settings = Settings()


