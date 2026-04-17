from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # JWT
    SECRET_KEY: str = "sPxPbP8G5OlYQFnNSboRHWp48eC4XTdukZqZZeKVCMc"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database
    DATABASE_URL: str = "sqlite:///./api_keys.db"
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 5
    REDIS_URL: Optional[str] = None
    
    # Admin
    ADMIN_SECRET_KEY: str = "admin_secret_key_12345"
    
    # App
    APP_NAME: str = "FastAPI Rate Limiting Service"
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()