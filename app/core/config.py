import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings (BaseSettings):
    API_VERSION: str = '/api/v1'
    PROJECT_NAME: str = 'Crime Detection App'
    DEBUG: bool = False
    # Get database_url from docker compose
    # DATABASE_URL: str = os.getenv('DATABASE_URL')
    DATABASE_URL: str
    POSTGRES_DB: str
    POSTGRES_USER:str
    POSTGRES_PASSWORD: str
    HOST_POSTGRES_PORT: int
    POSTGRES_HOST: str
    SECRET_KEY: str = ''
    # SECRET_KEY: str = os.getenv('SECRET_KEY')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    # CORS setting
    CORS_ORIGINS: list[str] = ["*"]

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

settings = Settings()