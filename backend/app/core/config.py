from typing import List
from pydantic import BaseSettings

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str
    EMAIL_RESET_TOKEN_EXPIRE_HOURS: float
    ACCESS_TOKEN_EXPIRE_MINUTES: float
    SECRET_KEY: str
    ALGORITHM: str
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost", "http://localhost:4200", "http://localhost:3000", "http://localhost:8080", "https://localhost", "https://localhost:4200", "https://localhost:3000", "https://localhost:8080"]
    PROJECT_NAME: str
    REDIS_PASSWORD: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()