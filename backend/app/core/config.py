from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    SECRET_KEY: str = "change-me-in-production"
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/umlaramigo"
    MONGODB_URL: str = "mongodb://umlaramigo:umlaramigo_password@localhost:27017/umlaramigo?authSource=admin"
    MONGODB_DB_NAME: str = "umlaramigo"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REPOSITORY_BACKEND: str = "sqlalchemy"  # 'sqlalchemy' ou 'mongodb'

    class Config:
        env_file = ".env"

settings = Settings()
