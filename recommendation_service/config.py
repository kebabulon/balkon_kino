from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DJANGO_API_BASE_URL: str = "http://localhost:8000/api"

    class Config:
        env_file = ".env"


settings = Settings()
