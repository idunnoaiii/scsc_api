from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    EMAIL_RESET_TOKEN_EXPIRE_HOURS: float
    SECRET_KEY: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


setting = Settings()