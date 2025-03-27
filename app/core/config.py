import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings (BaseSettings):
    API_VERSION: str = '/api/v1'
    PROJECT_NAME: str = 'Crime Detection App'
    DEBUG: bool = False
    # Get database_url from docker compose
    # DATABASE_URL: str = os.getenv('DATABASE_URL')
    DATABASE_URL: str
    SECRET_KEY: str = ''
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    # CORS setting
    CORS_ORIGINS: list[str] = ["*"]

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

settings = Settings()