"""Centralized configuration loaded from environment variables."""
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Application
    APP_NAME: str = "LeafGuard API"
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = False

    # Database
    POSTGRES_USER: str = "leafguard"
    POSTGRES_PASSWORD: str = "leafguard"
    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "leafguard"

    # Security
    SECRET_KEY: str = "change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    # Model
    MODEL_PATH: str = "ml/saved_models/leafguard_efficientnet.pt"
    CLASS_INDEX_PATH: str = "ml/saved_models/class_index.json"
    MODEL_INPUT_SIZE: int = 224

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
