"""
Central application settings, loaded from environment variables / .env file.
Import `settings` anywhere you need config instead of reading os.environ directly.
"""
import json
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "INTURI Portal API"
    API_V1_PREFIX: str = "/api/v1"

    DATABASE_URL: str

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    BACKEND_CORS_ORIGINS: str = "[]"

    MEDIA_ROOT: str = "./media"
    MAX_IMAGE_SIZE_MB: int = 5
    MAX_VIDEO_SIZE_MB: int = 50
    MAX_AUDIO_SIZE_MB: int = 15

    FIRST_ADMIN_EMAIL: str = "admin@gmail.com"
    FIRST_ADMIN_PASSWORD: str = "admin123"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

    @property
    def cors_origins_list(self) -> list[str]:
        try:
            return json.loads(self.BACKEND_CORS_ORIGINS)
        except (json.JSONDecodeError, TypeError):
            return []


settings = Settings()
